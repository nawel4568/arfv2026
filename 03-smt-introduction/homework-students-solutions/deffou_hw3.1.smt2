(set-option :produce-models true)

(declare-const a Int)
(declare-const b Int)
(declare-const c Int)

(define-fun is-digit ((x Real)) Bool (and (>= x 0) (<= x 9)))
(assert (is-digit a))
(assert (is-digit b))
(assert (is-digit c))

; a != 0 and c != 0
(assert (not (= a 0)))
(assert (not (= c 0)))

; abc and cba are multiples of 4
; i only took ba ad bc since it is the important parts for the division
(assert (= (mod (+ (* b 10) a) 4) 0))
(assert (= (mod (+ (* b 10) c) 4) 0))

(check-sat)
(get-model)