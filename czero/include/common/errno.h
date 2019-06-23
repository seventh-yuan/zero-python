/**
 * @file errno.h
 * @brief This is the difinition of errno.
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
#ifndef __COMMON_ERRNO_H__
#define __COMMON_ERRNO_H__

#define ENO_OK           (0)
#define ENO_ERROR        (-1)
#define ENO_TIMEOUT      (-2)
#define ENO_FULL         (-3)
#define ENO_EMPTY        (-4)
#define ENO_NOMEM        (-5)
#define ENO_BUSY         (-6)
#define ENO_INVAL        (-7)
#define ENO_INIT         (-8)

#ifdef __cplusplus
extern "C"{
#endif


#define RETURN_ERRNO(errno)         do { set_erno(errno); return errno; } while (0)

void set_errno(int errno);

/**
 * @brief get error reason.
 * @param errno error number.
 * @return error string has been found.
 */
const char* get_error_reason(void);

#ifdef __cplusplus
} // extern "C"
#endif
#endif // __COMMON_ERRNO_H__