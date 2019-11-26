-- Comment
{-
sadfasdf
-}

--import Data.List
--import System.IO


--main = putStrLn "Hello World!"

g = \y -> 3*3 + y*y

main = do
    print "Как вас зовут?"
    name <- getLine
    print ("Привет " ++ name ++ "!")

factorial n = if n > 1
              then n * factorial(n - 1)
              else 1


calc :: String -> Float
calc = head . foldl f [] . words
    where
        f :: [Float] -> String -> [Float]
        f (x:y:zs) "+"    = (y + x):zs
        f (x:y:zs) "-"    = (y - x):zs
        f (x:y:zs) "*"    = (y * x):zs
        f (x:y:zs) "/"    = (y / x):zs
        f (x:y:zs) "FLIP" = y:x:zs
        f (x:zs)   "ABS"  = (abs x):zs
        f xs       y      = read y : xs
