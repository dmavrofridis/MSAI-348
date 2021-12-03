(define (domain sokorobotto)
  (:requirements :typing)
  (:types  location shipment robot saleitem order pallette - object)
  (:predicates  
    (includes ?x - shipment ?y - saleitem)
    (orders ?x - order ?y - saleitem)
    (ships ?x - shipment ?y - order)
    (unstarted ?x - shipment)
    (contains ?x - pallette ?y - saleitem)
    (connected ?x - location ?y - location)
    (free ?x - robot)
    (packing-location ?x - location)
    (available ?x - location)
    (at ?x - object ?y - location)
    (no-pallette ?x - location)
    (no-robot ?x - location)
  )
  
      (:action robotMove
          :parameters (?r - robot ?location1 - location ?location2 - location)
          :precondition (and (at ?r ?location1)
                             (free ?r)
                             (no-robot ?location2)
                             (connected ?location1 ?location2)
                             )
          :effect (and
              (at ?r ?location2)
              (not (at ?r ?location1))
              (no-robot ?location1)
              (not (no-robot ?location2))
              
          )
      )
      
      (:action robotCarry
          :parameters (?r - robot ?location1 - location ?location2 - location ?p - pallette)
          :precondition (and (at ?r ?location1)
                             (free ?r)
                             (no-robot ?location2)
                             (connected ?location1 ?location2)
                             (at ?p ?location1)
                             (no-pallette ?location2)
                             )
          :effect (and
              (at ?r ?location2)
              (not (at ?r ?location1))
              (no-robot ?location1)
              (not (no-robot ?location2))
              (at ?p ?location2)
              (not (at ?p ?location1))
              (no-pallette ?location1)
              (not (no-pallette ?location2))
              
          )
      )
      
      (:action robotDeliver
          :parameters (?r - robot ?l - location ?p - pallette ?sp - shipment ?o - order ?sale_item - saleitem)
          :precondition (and 
                             (free ?r)
                             (at ?r ?l)
                             (at ?p ?l)
                             (packing-location ?l)
                             (contains ?p ?sale_item)
                             (orders ?o ?sale_item)
                             (ships ?sp ?o)
                             (unstarted ?sp)
                             (available ?l)
                             )
          :effect (and
              (includes ?sp ?sale_item)
              (not (contains ?p ?sale_item))
          )
      )
)