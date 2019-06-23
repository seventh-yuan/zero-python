/**
 * @file types.h
 * @brief This is the difinition of types.
 * @author yuanle
 * @version 0.1
 * @details Change history:
 * <Data>        |<Version>    |<Author>        |<Description>
 * -----------------------------------------------------------
 * 2019/05/30    |0.1          |yuanle          |Initial Version
 * -----------------------------------------------------------
 * @date 2019-05-30
 * @license Dual BSD/GPL
 */

#ifndef __COMMON_TYPES__
#define __COMMON_TYPES__

#ifdef __cplusplus
extern "C"{
#endif

typedef signed char                     ze_s8_t;    /**<  8bit integer type */
typedef unsigned char                   ze_u8_t;    /**<  8bit unsigned integer type */
typedef signed short                    ze_s16_t;   /**< 16bit integer type */
typedef unsigned short                  ze_u16_t;   /**< 32bit unsigned integer type */
typedef signed long                     ze_s32_t;   /**< 32bit integer type */
typedef unsigned long                   ze_u32_t;   /**< 32bit unsigned integer type */

typedef ze_u32_t                        ze_size_t;  /**< Type for size number */
typedef ze_s32_t                        ze_ssize_t; /**< Type for signed size number */

typedef ze_u32_t                        ze_base_t;
typedef ze_s8_t                         ze_err_t;
typedef ze_s32_t                        ze_result_t;

typedef ze_u32_t                        ze_tick_t;

typedef ze_u32_t                        ze_millis_t;
typedef ze_u32_t                        ze_usec_t;

typedef char                            ze_char_t;
typedef unsigned char                   ze_uchar_t;
typedef char*                           ze_string_t;
typedef const char*                     ze_const_string_t;

typedef enum {
    False = 0,
    True = 1
} ze_bool_t;

#define ze_U8_MAX                       0xFF
#define ze_U16_MAX                      0xFF
#define ze_U32_MAX                      0xFF

#define ze_TICK_MAX                     ze_U32_MAX      V

#if defined(__ICCARM__)
#define ze_volatile             volatile
#define ze_inline               static inline
#define ze_week                 __weak
#elif defined(__GNUC__)
#define ze_volatile             volatile
#define ze_inline               static __inline
#define ze_week                 __attribute__((weak))
#elif defined(__CC_ARM)
#define ze_volatile             __volatile
#define ze_inline               __inline
#define ze_week                 __weak
#endif

#define ALIGN(size, align)           (((size) + (align) - 1) & ~((align) - 1))

#define ALIGN_DOWN(size, align)      ((size) & ~((align) - 1))

#ifndef NULL
#define NULL                         (0)
#endif

#define CONTAINER_OF(node, type, member)\
    ((type *)((char *)(node) - (unsigned long)(&((type *)0)->member)))

#define BIT(b)    (1<<(b))

#define BIT_SET(x,b)            ((x)|=BIT(b))
#define BIT_RESET(x,b)          ((x)&=~(BIT(b)))
#define BITS_SET(x,bits)        ((x)|=bits)
#define BITS_RESET(x,bits)      ((x)&=~(bi/bits))
#define BIT_TEST(x,b)           (((x)&(BIT(b)))?1:0)
#define BITS_TEST(x,bits)       (((x)&(bits))?1:0)


#ifdef __cplusplus
} // extern "C"
#endif
#endif // __COMMON_TYPES_H__
