/**
 * @file assert.h
 * @brief This is the difinition of assert.
 * @author yuanle
 * @version 0.1
 * @details Change history:
 * <Data>        |<Version>    |<Author>        |<Description>
 * -----------------------------------------------------------
 * 2019/05/31    |0.1          |yuanle          |Initial Version
 * -----------------------------------------------------------
 * @date 2019-05-31
 * @license Dual BSD/GPL
 */
#ifndef __COMMON_ASSERT_H__
#define __COMMON_ASSERT_H__
#include <common/types.h>

#ifdef __cplusplus
extern "C"{
#endif

#if CONFIG_USING_ASSERT == 1
#define ASSERT(expr)     if(!(expr))\
                                do{\
                                    printf("file %s: line%d: function %s: Assertion '%s' failed\n",\
                                    __FILE__, __LINE__, __FUNCTION__, #expr);\
                                    while(1);\
                                }while(0)
#else
#define ASSERT(expr)     ((void)0) 
#endif

#ifdef __cplusplus
} // extern "C"
#endif
#endif // __COMMON_ASSERT_H__