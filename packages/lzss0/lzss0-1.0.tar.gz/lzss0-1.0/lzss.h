#ifndef LZSS_H
#define LZSS_H 1
#define LZSS_VERSION 1.0

// code cleanups, c++ compatibility, and algorithm parameters added
// thanks to,
//     Luigi Auriemma for the decompression algorithm,
//     and Haruhiko Okumura for the compression algorithm
//
// lvlrk 3/24/24

#ifdef __cplusplus
extern "C" {
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned int  uint;

struct lzss_param {
    uint EI;       // n reference offset bits
    uint EJ;       // n reference length bits
    uint P;        // output code threshold
    char init_chr; // initial buffer character
};

#define LZSS_PARAM  (struct lzss_param){12, 4, 2, ' '}
#define LZSS0_PARAM (struct lzss_param){12, 4, 2, 0}

enum lzss_window_type {
    LZSS_WINDOW_VESPERIA = 0xff,
    LZSS_WINDOW_FORWARD  = 0xfe,
    LZSS_WINDOW_BACKWARD = 0xfd
};

static void lzss_set_window(u8* window, uint window_size, int init_chr) {
    uint i = 0;
    int  n;

    switch(init_chr) {
    case LZSS_WINDOW_VESPERIA: // Tales of Vesperia (thanks to delguoqing)
        memset(window, 0, window_size);

        for(;; i++) {
            n = (i * 8) + 6;
            if(n >= window_size)
                break;

            window[n] = i;
        }

        break;
    case LZSS_WINDOW_FORWARD: // invented
        for(; i < window_size; i++)
            window[i] = i;

        break;
    case LZSS_WINDOW_BACKWARD: // invented
        for(i = window_size - 1; i >= 0; i--)
            window[i] = i;

        break;
    default:
        memset(window, init_chr, window_size);

        break;
    }
}

// returns n of decoded bytes;
#ifndef __cplusplus // C
static uint lzss_decompress(u8* src, uint srclen, u8* dst, uint dstlen, struct lzss_param param) {
#else              // C++
static uint lzss_decompress(u8* src, uint srclen, u8* dst, uint dstlen, struct lzss_param param=LZSS0_PARAM) {
#endif
    // MUST sum to 16 bits (or 2 bytes)
    uint EI     = param.EI; // typically 10..13
    uint EJ     = param.EJ; // typically 4..5

    uint P        = param.P; // if reference length <= P, output a character */
    uint rless    = P;       // in some rare implementations it could be 0
    char init_chr = param.init_chr;

    uint slide_winsz = 0;
    u8*  slide_win   = NULL;

    u8*  dststart    = dst;
    u8*  srcend      = src + srclen;
    u8*  dstend      = dst + dstlen;

    int i, j, k, r;
    u8 c; // temporary decoded byte
    unsigned flags;

    uint N = 1 << EI; // sliding window size
    uint F = 1 << EJ;

    r = (N - F) - rless;

    N--;
    F--;

    if(slide_winsz < N) {
#ifndef __cplusplus
        slide_win = realloc(slide_win, N);
#else
        slide_win = reinterpret_cast<u8*>(realloc(slide_win, N));
#endif
        if(!slide_win)
            return 0;

        slide_winsz = N;
    }
    lzss_set_window(slide_win, N, init_chr);

    for(flags = 0;; flags >>= 1) {
        if(!(flags & 0x100)) {
            if(src >= srcend)
                break;

            flags = *src++;
            flags |= 0xff00;
        } else if(flags & 1) { // uncoded byte
            if(src >= srcend)
                break;

            c = *src++;

            if(dst >= dstend)
                goto quit;

            *dst++ = c;

            slide_win[r] = c;
            r = (r + 1) & N;
        } else {               // coded byte
            if(src >= srcend)
                break;

            i = *src++;

            if(src >= srcend)
                break;

            j = *src++;

            i |= ((j >> EJ) << 8); // take reference offset
            j  = (j & F) + P;      // take reference length

            // write coded reference to dst
            for(k = 0; k <= j; k++) {
                c = slide_win[(i + k) & N];

                if(dst >= dstend)
                    goto quit;

                *dst++ = c;

                // move in sliding window
                slide_win[r] = c;
                r = (r + 1) & N;
            }
        }
    }
quit:
    return (dst - dststart);
}

// modified by Luigi Auriemma
/**************************************************************
	LZSS.C -- A Data Compression Program
	(tab = 4 spaces)
***************************************************************
	4/6/1989 Haruhiko Okumura
	Use, distribute, and modify this program freely.
	Please send me your improved versions.
		PC-VAN		SCIENCE
		NIFTY-Serve	PAF01022
		CompuServe	74050,1022
**************************************************************/

// reformatting this code gave me
// hemorrhoids, aids, and an aneurysm

// i <3 Haruhiko Okumura

static uint N         =	4096; // size of ring buffer
static uint F         =	18;	  // upper limit for match_length
static uint THRESHOLD =	2;    // encode string into position and length
						      // if match_length is greater than this

static int  NIL; // index for root of binary search trees
static char init_chr;

static uint textsize = 0; // text size counter
static uint codesize = 0; // code size counter

static u8* text_buf = NULL; // ring buffer of size N
			                // with extra F-1 bytes to facilitate string comparison

static int match_position, // of longest match.  These are
           match_length;   // set by the InsertNode() procedure.

// left & right children &
// parents -- These constitute binary search trees.
static int *lson = NULL,
           *rson = NULL,
           *dad  = NULL;

static u8 *infile   = NULL,
          *infilel  = NULL,
          *outfile  = NULL,
          *outfilel = NULL;

static inline int lzss_xgetc() {
    if(infile >= infilel)
        return -1;

    return *infile++;
}

static inline int lzss_xputc(int chr) {
    if(outfile >= outfilel)
        return -1;

    *outfile++ = chr;

    return chr;
}

/* For i = 0 to N - 1, rson[i] and lson[i] will be the right and
 * left children of node i.  These nodes need not be initialized.
 * Also, dad[i] is the parent of node i.  These are initialized to
 * NIL (= N), which stands for 'not used.'
 * For i = 0 to 255, rson[N + i + 1] is the root of the tree
 * for strings that begin with character i.  These are initialized
 * to NIL.  Note there are 256 trees.
 */
static void lzss_init_tree() {
	int i;

	for(i = N + 1; i <= N + 256; i++)
        rson[i] = NIL;

	for(i = 0; i < N; i++)
        dad[i] = NIL;
}

/* Inserts string of length F, text_buf[r..r+F-1], into one of the
 * trees (text_buf[r]'th tree) and returns the longest-match position
 * and length via the global variables match_position and match_length.
 * If match_length = F, then removes the old node in favor of the new
 * one, because the old one will be deleted sooner.
 * Note r plays double role, as tree node and position in buffer.
 */
static void lzss_insert_node(int r) {
	int i;
    u8* key = &text_buf[r];
    int p = N + 1 + key[0];
    int cmp = 1;

    match_length = 0;

	rson[r] = lson[r] = NIL;

	for(;;) {
		if(cmp >= 0) {
            // right side
			if(rson[p] != NIL) {
                p = rson[p];
            } else {
                rson[p] = r;
                dad[r] = p;

                return;
            }
		} else {
            // left side
			if(lson[p] != NIL) {
                p = lson[p];
            } else {
                lson[p] = r;
                dad[r] = p;

                return;
            }
		}

		for(i = 1; i < F; i++) {
			if((cmp = key[i] - text_buf[p + i]) != 0)
                break;
        }

		if(i > match_length) {
			match_position = p;

			if((match_length = i) >= F)
                break;
		}
	}

	dad[r] = dad[p];
    lson[r] = lson[p]; rson[r] = rson[p];

	dad[lson[p]] = r; dad[rson[p]] = r;

	if(rson[dad[p]] == p) {
        rson[dad[p]] = r;
    } else { 
        lson[dad[p]] = r;
    }

	dad[p] = NIL; // remove p
}

// deletes node p from tree
static void lzss_delete_node(int p) {
	int q;
	
    // not in tree
	if(dad[p] == NIL)
        return;

	if(rson[p] == NIL) {
        q = lson[p];
    } else if(lson[p] == NIL) {
        q = rson[p];
    } else {
		q = lson[p];

		if(rson[q] != NIL) {
			do {
                q = rson[q];
            } while(rson[q] != NIL);

			rson[dad[q]] = lson[q]; dad[lson[q]] = dad[q];
			lson[q] = lson[p]; dad[lson[p]] = q;
		}

		rson[q] = rson[p];
        dad[rson[p]] = q;
	}

	dad[q] = dad[p];
	if(rson[dad[p]] == p) {
        rson[dad[p]] = q;
    } else {
        lson[dad[p]] = q;
    }

	dad[p] = NIL;
}

static void lzss_encode() {
	int i, c, r, s;
    int len, last_match_length, code_buf_ptr;
	u8 code_buf[17], mask;
	
	lzss_init_tree();

    /* code_buf[1..16] saves eight units of code, and
	 * code_buf[0] works as eight flags, "1" representing that the unit
	 * is an unencoded letter (1 byte), "0" a position-and-length pair
	 * (2 bytes).  Thus, eight units require at most 16 bytes of code.
     */
	code_buf[0] = 0;

    code_buf_ptr = mask = 1;
	s = 0;
    r = N - F;

    lzss_set_window(text_buf, r, init_chr);

	for(len = 0; len < F && (c = lzss_xgetc()) != EOF; len++)
		text_buf[r + len] = c; // Read F bytes into buffer's last F bytes

	if((textsize = len) == 0)
        return;

    /* Insert the F strings,
	 * each of which begins with one or more 'space' characters.  Note
	 * the order in which these strings are inserted.  This way,
	 * degenerate trees will be less likely to occur. 
     */
	for(i = 1; i <= F; i++) 
        lzss_insert_node(r - i);

    lzss_insert_node(r); // Finally, insert the whole string just read

	do {
        // match_length may be spuriously long near the end of text
		if(match_length > len)
            match_length = len;

        if(match_length <= THRESHOLD) {
			match_length = 1; // Not long enough match; send one byte

			code_buf[0]              |= mask;        // 'send one byte' flag
			code_buf[code_buf_ptr++]  = text_buf[r]; // Send uncoded
		} else {
			code_buf[code_buf_ptr++] = (u8)match_position;

            // Send position and length pair.
            // Note, match_length > THRESHOLD.
			code_buf[code_buf_ptr++] =
                (u8)(((match_position >> 4) & 0xf0) |
                (match_length - (THRESHOLD + 1)));
        }

        // shift mask left 1 bit
		if((mask <<= 1) == 0) {
            // send at most 1 byte
			for(i = 0; i < code_buf_ptr; i++)
				lzss_xputc(code_buf[i]);

			codesize += code_buf_ptr;

			code_buf[0]  = 0;
            code_buf_ptr = mask = 1;
		}

		last_match_length = match_length;
		for(i = 0; i < last_match_length &&
				(c = lzss_xgetc()) != EOF; i++) {

			lzss_delete_node(s); // delete old strings
			text_buf[s] = c;     // read new bytes

            /* If the position is
			 * near the end of buffer, extend the buffer to make
			 * string comparison easier.
             */

			if(s < F - 1)
                text_buf[s + N] = c;

			s = (s + 1) & (N - 1);
            r = (r + 1) & (N - 1);

			lzss_insert_node(r); // Register the string in text_buf[r..r+F-1]
		}

        // after the end of text
		while (i++ < last_match_length) {
			lzss_delete_node(s);

			s = (s + 1) & (N - 1);
            r = (r + 1) & (N - 1);

			if(--len)
                lzss_insert_node(r); // buffer may not be empty
		}
	} while(len > 0); // until length of string to be processed is zero

    // send remaining code
	if(code_buf_ptr > 1) {
		for(i = 0; i < code_buf_ptr; i++)
            lzss_xputc(code_buf[i]);

		codesize += code_buf_ptr;
	}
}

// returns n of coded bytes;
#ifndef __cplusplus
static uint lzss_compress(u8* src, uint srclen, u8* dst, uint dstlen, struct lzss_param param) {
#else
static uint lzss_compress(u8* src, uint srclen, u8* dst, uint dstlen, struct lzss_param param=LZSS0_PARAM) {
#endif
    infile   = src;
    infilel  = src + srclen;
    outfile  = dst;
    outfilel = dst + dstlen;

    NIL = N;
#ifndef __cplusplus
    text_buf = realloc(text_buf, N + F - 1);
    lson     = realloc(lson, sizeof(int) * (N + 1));
    rson     = realloc(rson, sizeof(int) * (N + 257));
    dad      = realloc(dad,  sizeof(int) * (N + 1));
#else
    // youd think c++ would at least be lenient with
    // void* pointers, but no. c++ has to be fussy.
    // why cant you be cool like your older brother, C?
    text_buf = reinterpret_cast<u8*>(realloc(text_buf, N + F - 1));
    lson     = reinterpret_cast<int*>(realloc(lson, sizeof(int) * (N + 1)));
    rson     = reinterpret_cast<int*>(realloc(rson, sizeof(int) * (N + 257)));
    dad      = reinterpret_cast<int*>(realloc(dad, sizeof(int) * (N + 1)));
#endif
   
    // set parameters before encoding
    N         = 1 << param.EI;
    F         = 1 << param.EJ;
    THRESHOLD = param.P;
    init_chr  = param.init_chr;

    lzss_encode();

    return(outfile - dst);
}
#ifdef __cplusplus
}
#endif
#endif
