(set-option :produce-models true)

; the variables are defined by position+number
; for example: p12 is password with number 2 in  position 1 
(declare-const p11 Bool)
(declare-const p12 Bool)
(declare-const p13 Bool)
(declare-const p14 Bool)
(declare-const p21 Bool)
(declare-const p22 Bool)
(declare-const p23 Bool)
(declare-const p24 Bool)
(declare-const p31 Bool)
(declare-const p32 Bool)
(declare-const p33 Bool)
(declare-const p34 Bool)

; The password should be even
(assert (xor p32 p34))

; We cannot use the same digit three times, otherwise it would be easy to guess it.
(assert (and
	(or (not p11)(not p21)(not p31))
	(or (not p12)(not p22)(not p32))
	(or (not p13)(not p23)(not p33))
	(or (not p14)(not p24)(not p34))
))

; It is possible to repeat the same digit twice, just make sure the two degits are not adjecent.
(assert (=> p21 (and (not p11) (not p31)))) 
(assert (=> p22 (and (not p12) (not p32)))) 
(assert (=> p23 (and (not p13) (not p33)))) 
(assert (=> p24 (and (not p14) (not p34))))

; hidden condition: at least one digit per position
(assert (and
	(or p11 p12 p13 p14)
	(or p21 p22 p23 p24)
	(or p31 p32 p33 p34)
))

; at most one per position:
(assert (and
	 (=> p11 (not (or p12 p13 p14)))
	 (=> p12 (not (or p11 p13 p14)))
	 (=> p13 (not (or p12 p11 p14)))
	 (=> p14 (not (or p12 p13 p11)))))
(assert (and
	 (=> p21 (not (or p22 p23 p24)))
	 (=> p22 (not (or p21 p23 p24)))
	 (=> p23 (not (or p22 p21 p24)))
	 (=> p24 (not (or p22 p23 p21)))))
(assert (and
	 (=> p31 (not (or p32 p33 p34)))
	 (=> p32 (not (or p31 p33 p34)))
	 (=> p33 (not (or p32 p31 p34)))
	 (=> p34 (not (or p32 p33 p31)))))
	 
; checking if the password 434 is unique
(assert (or (not p14) (not p23) (not p34)))

; The model returns SAT after the checking !(434) means this password is not unique
(check-sat) 
(get-model)
(exit)
