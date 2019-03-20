
(let zero? (fn (x) (if x 0 1)))

(let nil? (fn (x) (= x nil)))

(let cons 
  (fn (x y)
      (fn (msg)
          (if (= msg "head") x y))))

(let head 
  (fn (cell)
      (cell "head")))

(let tail
  (fn (cell)
      (cell "tail")))

(let printl
  (fn (xs)
      (begin
        (print "[")
        (print-list xs)
        (println "]"))))

(let print-list
  (fn (l)
      (if (= l nil) 
        nil
        (begin
          (print (head l))
          (print-list (tail l))))))

(let reduce
  (fn (f i xs)
    (if (nil? xs) 
      i
      (f (head xs) (reduce f i (tail xs))))))

(let map
  (fn (f xs)
      (reduce (fn (x y) (cons (f x) y))
              nil
              xs)))

(let filter
  (fn (pred xs)
      (if (nil? xs) nil
        (if (pred (head xs))
          (cons (head xs) (filter pred (tail xs)))
          (filter pred (tail xs))))))

(let even? 
  (fn (x)
      (if (= 0 (% x 2)) 1 0)))

(let square (fn (x) (* x x)))

(let sum-square-evens
  (fn [xs]
      (reduce + 0
      (map square
      (filter even? xs)))))

(let xs (cons 1 (cons 2 (cons 3 (cons 4 (cons 5 (cons 6 nil)))))))

(println (sum-square-evens xs))


