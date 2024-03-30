#ifndef LZSS_H
#define LZSS_H
#define LZSS_VERSION 1.0
#define LZSS_DEBUG 0

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

typedef unsigned char  uchar;
typedef unsigned short ushort;
typedef unsigned int   uint;

struct lzss_param {
    uint  EI;       // n code offset bits
    uint  EJ;       // n code length bits
    uint  P;        // output text threshold
    uchar init_chr; // initial sliding window character
};

enum lzss_window_type {
    LZSS_WINDOW_VESPERIA = 0xff,
    LZSS_WINDOW_FORWARD  = 0xfe,
    LZSS_WINDOW_BACKWARD = 0xfd
};

static void lzss_set_window(uchar* window, uint window_size, uchar init_chr) {
    uint i = 0;
    uint n; // vesperia value

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
static uint lzss_decompress(uchar* src, uint srclen, uchar* dst, uint dstlen, struct lzss_param param) {
    if((param.EI + param.EJ) != 16)
        return 0;

    // parameters
    uint  EI       = param.EI;       // n code offset bits
    uint  EJ       = param.EJ;       // n code length bits
    uint  P        = param.P;        // reference length <= P, output decoded symbol
    uchar init_chr = param.init_chr; // initial sliding window character

    // bitmasks
    uint N = 1 << EI; // sliding window size & bitmask
    uint F = 1 << EJ; // code length bitmask

    // sliding window
    uchar* slide_win = (uchar*)malloc(N);
    if(!slide_win)
        return 0;
    lzss_set_window(slide_win, N, init_chr);

    ushort  i, // first   code byte (offset)
            j; // second  code byte (length)
    uint    k; // current code index
    uchar   c; // current symbol

    uint r     = (N - F) - P, // sliding window index
         flags = 0;           // is symbol coded?

    // buffers
    uchar* dststart = dst;          // to calculate n decoded bytes
    uchar* srcend   = src + srclen; // coded buffer overrun check
    uchar* dstend   = dst + dstlen; // uncoded buffer overrun check
    
    N--; F--; // decremented for bitmasking

    for(;; flags >>= 1) {
        if(!(flags & 0x100)) {
            if(src >= srcend)
                break;
            flags  = *src++;
            flags |= 0xff00;
        }
        if(flags & 1) { // uncoded symbol
            if(src >= srcend)
                break;
            c = *src++;

            if(dst >= dstend)
                goto quit;
            *dst++ = c;

            slide_win[r] = c;
            r            = (r + 1) & N;
        } else { // coded symbol
            if(src >= srcend)
                break;
            i = *src++;

            if(src >= srcend)
                break;
            j = *src++;

            i |= ((j >> EJ) << 8); // get code offset
            j  = (j & F) + P;      // get code length

            // write symbols to text
            for(k = 0; k <= j; k++) {
                c = slide_win[(i + k) & N];

                if(dst >= dstend)
                    goto quit;
                *dst++ = c;

                slide_win[r] = c;
                r            = (r + 1) & N;
            }
        }
    }
quit:
    free(slide_win);

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

static uint N;         // size of ring buffer
static uint F;         // upper limit for match_length
static uint THRESHOLD; // encode string into position and length
					   // if match_length is greater than this

static int  NIL;      // index for root of binary search trees
static int  init_chr; // initial buffer character

static uint textsize = 0; // text size counter
static uint codesize = 0; // code size counter

static uchar* text_buf = NULL; // ring buffer of size N
			                // with extra F-1 bytes to facilitate string comparison

static int match_position, // of longest match.  These are
           match_length;   // set by the InsertNode() procedure.

// left & right children &
// parents -- These constitute binary search trees.
static int *lson = NULL,
           *rson = NULL,
           *dad  = NULL;

static uchar *infile   = NULL,
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
    uchar* key = &text_buf[r];
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
	uchar code_buf[17], mask;
	
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
			code_buf[code_buf_ptr++] = (uchar)match_position;

            // Send position and length pair.
            // Note, match_length > THRESHOLD.
			code_buf[code_buf_ptr++] =
                (uchar)(((match_position >> 4) & 0xf0) |
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
static uint lzss_compress(uchar* src, uint srclen, uchar* dst, uint dstlen, struct lzss_param param) {
    infile   = src;
    infilel  = src + srclen;
    outfile  = dst;
    outfilel = dst + dstlen;

    // set parameters before encoding
    N         = 1 << param.EI;
    F         = (1 << param.EJ) + param.P;
    THRESHOLD = param.P;
    init_chr  = param.init_chr;
    NIL       = N;

    text_buf = (uchar*)realloc(text_buf, N + F - 1);
    lson     = (int*)realloc(lson, sizeof(int) * (N + 1));
    rson     = (int*)realloc(rson, sizeof(int) * (N + 257));
    dad      = (int*)realloc(dad, sizeof(int) * (N + 1));

    lzss_encode();

    return(outfile - dst);
}
#ifdef __cplusplus
}
#endif
#endif
