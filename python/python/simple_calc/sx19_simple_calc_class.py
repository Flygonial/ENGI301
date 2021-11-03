# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Simple Calculator
--------------------------------------------------------------------------
License:   
Copyright 2021 <NAME>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Simple calculator that will 
  - Take in two numbers from the user
  - Take in an operator from the user
  - Perform the mathematical operation and provide the number to the user
  - Repeat

Operations:
  - addition
  - subtraction
  - multiplication
  - division

Error conditions:
  - Invalid operator --> Program should exit
  - Invalid number   --> Program should exit

--------------------------------------------------------------------------
"""
import operator

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# Not applicable

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

operators = {
    "+"  : operator.add,
    "-"  : operator.sub,
    "*"  : operator.mul,
    "/"  : operator.truediv,
    "<<" : operator.lshift,
    ">>" : operator.rshift,
    "**" : operator.pow,
    "%"  : operator.mod
}

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def get_user_input():
    """Get input from the user:  two numbers and operator."""
    
    try:
        operator = input("Enter the operator (valid operators are +, -, *, /, <<, >>, **, and %): ")
        # Again, case of lshift or rshift
        if operator == '>>' or '<<':
            number1  = int(input("Enter the first number:  "))
            number2  = int(input("Enter the second number: "))
        
        else:
            number1  = float(input("Enter the first number:  "))
            number2  = float(input("Enter the second number: "))
    
        return (number1, number2, operator)
        
    except:
        print("Invalid Input")
        return (None, None, None)

# End def


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == "__main__":
    
    while True:
        # Get user input
        (number1, number2, operator) = get_user_input()

        # Get function to execute from operators dictionary
        function = operators.get(operator, None)

        # Check if there was an error; Exit the program        
        if (number1 is None) or (number2 is None) or (function is None):
            print("Exiting")
            break

        # Calculate results and print result
        print(function(number1, number2))
    