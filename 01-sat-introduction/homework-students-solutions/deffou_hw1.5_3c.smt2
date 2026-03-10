(set-option :produce-models true)

; there is three degits which are the three colors, so we give each node
; a number (1 2 3)
(declare-const A1 Bool)
(declare-const A2 Bool)
(declare-const A3 Bool)
(declare-const B1 Bool)
(declare-const B2 Bool)
(declare-const B3 Bool)
(declare-const C1 Bool)
(declare-const C2 Bool)
(declare-const C3 Bool)
(declare-const D1 Bool)
(declare-const D2 Bool)
(declare-const D3 Bool)

; A -- B
(assert (not (and A1 B1)))
(assert (not (and A2 B2)))
(assert (not (and A3 B3)))
; A -- C
(assert (not (and A1 C1)))
(assert (not (and A2 C2)))
(assert (not (and A3 C3)))
; A -- D
(assert (not (and A1 D1)))
(assert (not (and A2 D2)))
(assert (not (and A3 D3)))

; B -- C
(assert (not (and B1 C1)))
(assert (not (and B2 C2)))
(assert (not (and B3 C3)))

; C -- D
(assert (not (and C1 D1)))
(assert (not (and C2 D2)))
(assert (not (and C3 D3)))

; Hidden conditions:
(assert (=> A1 (and (not A2) (not A3))))
(assert (=> B1 (and (not B2) (not B3))))
(assert (=> C1 (and (not C2) (not C3))))
(assert (=> D1 (and (not D2) (not D3))))

(assert (and
	(or A1 A2 A3)
	(or B1 B3 B3)
	(or C1 C3 C3)
	(or D1 D2 D3)
))

; It is possible to 3 color the graph (A2, B1, C3, D1) 

(check-sat)
(get-model)
(exit)

