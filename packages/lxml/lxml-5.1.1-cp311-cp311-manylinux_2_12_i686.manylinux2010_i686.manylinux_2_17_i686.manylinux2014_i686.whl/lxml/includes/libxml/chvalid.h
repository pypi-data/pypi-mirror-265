/*
 * Summary: Unicode character range checking
 * Description: this module exports interfaces for the character
 *               range validation APIs
 *
 * This file is automatically generated from the cvs source
 * definition files using the genChRanges.py Python script
 *
 * Generation date: Mon Mar 27 11:09:48 2006
 * Sources: chvalid.def
 * Author: William Brack <wbrack@mmm.com.hk>
 */

#ifndef __XML_CHVALID_H__
#define __XML_CHVALID_H__

#include <libxml/xmlversion.h>
#include <libxml/xmlstring.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Define our typedefs and structures
 *
 */
typedef struct _xmlChSRange xmlChSRange;
typedef xmlChSRange *xmlChSRangePtr;
struct _xmlChSRange {
    unsigned short	low;
    unsigned short	high;
};

typedef struct _xmlChLRange xmlChLRange;
typedef xmlChLRange *xmlChLRangePtr;
struct _xmlChLRange {
    unsigned int	low;
    unsigned int	high;
};

typedef struct _xmlChRangeGroup xmlChRangeGroup;
typedef xmlChRangeGroup *xmlChRangeGroupPtr;
struct _xmlChRangeGroup {
    int			nbShortRange;
    int			nbLongRange;
    const xmlChSRange	*shortRange;	/* points to an array of ranges */
    const xmlChLRange	*longRange;
};

/**
 * Range checking routine
 */
XMLPUBFUN int
		xmlCharInRange(unsigned int val, const xmlChRangeGroup *group);


/**
 * xmlIsBaseChar_ch:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsBaseChar_ch(c)	(((0x41 <= (c)) && ((c) <= 0x5a)) || \
				 ((0x61 <= (c)) && ((c) <= 0x7a)) || \
				 ((0xc0 <= (c)) && ((c) <= 0xd6)) || \
				 ((0xd8 <= (c)) && ((c) <= 0xf6)) || \
				  (0xf8 <= (c)))

/**
 * xmlIsBaseCharQ:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsBaseCharQ(c)	(((c) < 0x100) ? \
				 xmlIsBaseChar_ch((c)) : \
				 xmlCharInRange((c), &xmlIsBaseCharGroup))

XMLPUBVAR const xmlChRangeGroup xmlIsBaseCharGroup;

/**
 * xmlIsBlank_ch:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsBlank_ch(c)	(((c) == 0x20) || \
				 ((0x9 <= (c)) && ((c) <= 0xa)) || \
				 ((c) == 0xd))

/**
 * xmlIsBlankQ:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsBlankQ(c)		(((c) < 0x100) ? \
				 xmlIsBlank_ch((c)) : 0)


/**
 * xmlIsChar_ch:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsChar_ch(c)		(((0x9 <= (c)) && ((c) <= 0xa)) || \
				 ((c) == 0xd) || \
				  (0x20 <= (c)))

/**
 * xmlIsCharQ:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsCharQ(c)		(((c) < 0x100) ? \
				 xmlIsChar_ch((c)) :\
				(((0x100 <= (c)) && ((c) <= 0xd7ff)) || \
				 ((0xe000 <= (c)) && ((c) <= 0xfffd)) || \
				 ((0x10000 <= (c)) && ((c) <= 0x10ffff))))

XMLPUBVAR const xmlChRangeGroup xmlIsCharGroup;

/**
 * xmlIsCombiningQ:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsCombiningQ(c)	(((c) < 0x100) ? \
				 0 : \
				 xmlCharInRange((c), &xmlIsCombiningGroup))

XMLPUBVAR const xmlChRangeGroup xmlIsCombiningGroup;

/**
 * xmlIsDigit_ch:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsDigit_ch(c)	(((0x30 <= (c)) && ((c) <= 0x39)))

/**
 * xmlIsDigitQ:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsDigitQ(c)		(((c) < 0x100) ? \
				 xmlIsDigit_ch((c)) : \
				 xmlCharInRange((c), &xmlIsDigitGroup))

XMLPUBVAR const xmlChRangeGroup xmlIsDigitGroup;

/**
 * xmlIsExtender_ch:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsExtender_ch(c)	(((c) == 0xb7))

/**
 * xmlIsExtenderQ:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsExtenderQ(c)	(((c) < 0x100) ? \
				 xmlIsExtender_ch((c)) : \
				 xmlCharInRange((c), &xmlIsExtenderGroup))

XMLPUBVAR const xmlChRangeGroup xmlIsExtenderGroup;

/**
 * xmlIsIdeographicQ:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsIdeographicQ(c)	(((c) < 0x100) ? \
				 0 :\
				(((0x4e00 <= (c)) && ((c) <= 0x9fa5)) || \
				 ((c) == 0x3007) || \
				 ((0x3021 <= (c)) && ((c) <= 0x3029))))

XMLPUBVAR const xmlChRangeGroup xmlIsIdeographicGroup;
XMLPUBVAR const unsigned char xmlIsPubidChar_tab[256];

/**
 * xmlIsPubidChar_ch:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsPubidChar_ch(c)	(xmlIsPubidChar_tab[(c)])

/**
 * xmlIsPubidCharQ:
 * @c: char to validate
 *
 * Automatically generated by genChRanges.py
 */
#define xmlIsPubidCharQ(c)	(((c) < 0x100) ? \
				 xmlIsPubidChar_ch((c)) : 0)

XMLPUBFUN int
		xmlIsBaseChar(unsigned int ch);
XMLPUBFUN int
		xmlIsBlank(unsigned int ch);
XMLPUBFUN int
		xmlIsChar(unsigned int ch);
XMLPUBFUN int
		xmlIsCombining(unsigned int ch);
XMLPUBFUN int
		xmlIsDigit(unsigned int ch);
XMLPUBFUN int
		xmlIsExtender(unsigned int ch);
XMLPUBFUN int
		xmlIsIdeographic(unsigned int ch);
XMLPUBFUN int
		xmlIsPubidChar(unsigned int ch);

#ifdef __cplusplus
}
#endif
#endif /* __XML_CHVALID_H__ */
