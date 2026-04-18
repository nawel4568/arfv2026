(set-option :produce-models true)

(declare-const yellow Int)
(declare-const red Int)
(declare-const green Int)
(declare-const blue Int)

(define-const tmp1 Int (* red 2))
(define-const tmp2 Int (+ green blue))
(define-const tmp3 Int (+ green red))
(define-const tmp4 Int (+ (* 3 yellow) green))
(define-const tmp5 Int (* 2 yellow))

(assert (= tmp1 tmp2))
(assert (= tmp3 tmp4))
(assert (= (+ tmp1 tmp2 tmp5) (+ tmp3 tmp4)))
(assert (= (+ tmp1 tmp2 tmp5 tmp3 tmp4) 56))

; Solution is
; yellow = 2
; red = 6
; green = 8
; blue = 8

; (assert (= (+ tmp1 tmp2 tmp5 tmp3 tmp4) 58))

; if we impose the sum to be 58 the problem becomes unsat

(check-sat)
(get-model)