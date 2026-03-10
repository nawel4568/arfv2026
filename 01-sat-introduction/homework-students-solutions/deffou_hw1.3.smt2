(set-option :produce-models true)

; students, 'True' for guilty and 'False' for innocent
(declare-const A Bool)
(declare-const B Bool)
(declare-const C Bool)

; A said: "B is guilty and C is innocent"
(assert (and B (not C)))

; B said: "if A is guilty, then C is also guilty"
(assert (=> A C))

; C said: "I'm innocent and one of the others, perhaps even the two, are guilty"
(assert (and (not C) (or A B)))

; B is guilty.
(check-sat)
(get-model)
(exit)
