(set-option :produce-models true)

; The two colors are True and False
(declare-const A Bool)
(declare-const B Bool)
(declare-const C Bool)
(declare-const D Bool)

; A -- B, A -- C, A -- D
(assert (and
	(xor A B)
	(xor A C)
	(xor A D)
))

; B -- C 
(assert (xor B C))

; C -- D
(assert (xor C D))

; It is not possible to color the graph using only 2 colors

(check-sat) 
(get-model)
(exit)
