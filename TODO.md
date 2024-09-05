##### Decimal to Float
0. Special values
 - 0
 - infinity
 - denormalized
 - NaN
1. Determine sign bit
 - (+) -> 0
 - (-) -> 1
2. Convert num to binary
 - abs(num)
 - position of binary point (exponent)
    - log2(num)
 - mantissa limit (round)
    - different methods
3. Shift point
 a. right (extra right 0s)
 b. within
 c. left (extra left 0s)
4. Add bias and convert to binary
5. Assemble floating point structure
 - remove first 1 in mantissa

##### Float to Decimal
-1. Determine precision
1. Break binary
 - sign
 - exponent
 - mantissa
1a. Special values
 - 0
 - infinity
 - denormalized
 - NaN
2. Add first 1 in mantissa
3. Remove exponent bias
5. Shift point
4. Convert back into decimal