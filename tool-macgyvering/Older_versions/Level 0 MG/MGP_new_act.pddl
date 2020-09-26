(define (domain MGP_new_act)
	(:requirements :strips)
	(:types htype - object)
    (:predicates
		(have ?what)
		(hammered ?what))
		
	(:action pick
		:parameters (?what)
		:precondition (not (have ?what))                       
		:effect (have ?what)
    )
	
	(:action hammer
		:parameters (?with - htype ?on)
		:precondition (have ?what)
		:effect (hammered ?on)
	)
)