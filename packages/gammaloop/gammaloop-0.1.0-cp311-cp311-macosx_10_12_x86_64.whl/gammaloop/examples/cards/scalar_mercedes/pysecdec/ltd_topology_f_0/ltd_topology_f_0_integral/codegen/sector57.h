* The name of the loop integral
#define name "ltd_topology_f_0_integral"

* Whether or not we are producing code for contour deformation
#define contourDeformation "0"

* Whether or not complex return type is enforced
#define enforceComplex "0"

* number of integration variables
#define numIV "6"

* number of regulators
#define numReg "1"

#define integrationVariables "x1,x2,x3,x4,x5,x6"
#define realParameters "p11,p12,p22"
#define complexParameters ""
#define regulators "eps"
Symbols `integrationVariables'
        `realParameters'
        `complexParameters'
        `regulators';

#define defaultQmcTransform "korobov3x3"

* Define the imaginary unit in sympy notation.
Symbol I;

#define calIDerivatives "SecDecInternalCalI"
#define functions "`calIDerivatives',SecDecInternalRemainder,SecDecInternalOtherPoly0"
CFunctions `functions';

#define decomposedPolynomialDerivatives "F,U"
CFunctions `decomposedPolynomialDerivatives';

* Temporary functions and symbols for replacements in FORM
AutoDeclare CFunctions SecDecInternalfDUMMY;
AutoDeclare Symbols SecDecInternalsDUMMY;

* We generated logs in the subtraction and pack denominators
* and powers into a functions.
CFunctions log, SecDecInternalPow, SecDecInternalDenominator;

* We rewrite function calls as symbols
#Do function = {`functions',`decomposedPolynomialDerivatives',log,SecDecInternalPow,SecDecInternalDenominator}
  AutoDeclare Symbols SecDecInternal`function'Call;
#EndDo

* We need labels for the code optimization
AutoDeclare Symbols SecDecInternalLabel;

* The integrand may be longer than FORM can read in one go.
* We use python to split the the expression if neccessary.
* Define a procedure that defines the "integrand" expression
#procedure defineExpansion
  Global expansion = SecDecInternalsDUMMYIntegrand;
    Id SecDecInternalsDUMMYIntegrand = (( + (( + (1)) * (( + (1))^(-1)))) * ( + (((( + (1)*x1*x2^4*x3^5)^( + (1))) * (( + ( + (1))*x2*x3^2)^( + (0) + (-1))) * (( + ( + (1))*x1*x2^2*x3^3)^( + (0) + (-1))) * (( + (1))^( + (1)))) * (SecDecInternalCalI( + (1)*x1, + (1)*x2, + (1)*x3, + (1)*x4, + (1)*x5, + (1)*x6, + (0))))));

#endProcedure

#define highestPoles "0"
#define requiredOrders "0"
#define numOrders "1"

* Specify and enumerate all occurring orders in python.
* Define the preprocessor variables
* `shiftedRegulator`regulatorIndex'PowerOrder`shiftedOrderIndex''.
#define shiftedRegulator1PowerOrder1 "0"

* Define two procedures to open and close a nested argument section
#procedure beginArgumentDepth(depth)
  #Do recursiveDepth = 1, `depth'
    Argument;
  #EndDo
#endProcedure
#procedure endArgumentDepth(depth)
  #Do recursiveDepth = 1, `depth'
    EndArgument;
  #EndDo
#endProcedure

* Define procedures to insert the dummy functions introduced in python and their derivatives.
#procedure insertCalI
    Id SecDecInternalCalI(x1?,x2?,x3?,x4?,x5?,x6?,eps?) = ( + (2)) * ((U( + (1)*x1, + (1)*x2, + (1)*x3, + (1)*x4, + (1)*x5, + (1)*x6, + (1)*eps)) ^ ( + (-1) + (4)*eps)) * ((F( + (1)*x1, + (1)*x2, + (1)*x3, + (1)*x4, + (1)*x5, + (1)*x6, + (1)*eps)) ^ ( + (-1) + (-3)*eps));

#endProcedure

#procedure insertOther
    Id SecDecInternalRemainder(x1?,x2?,x3?,x4?,x5?,x6?,eps?) =  + (1);
  Id SecDecInternalOtherPoly0(x1?,x2?,x3?,x4?,x5?,x6?,eps?) =  + ( + (1));

#endProcedure

#procedure insertDecomposed
    Id F(x1?,x2?,x3?,x4?,x5?,x6?,eps?) =  + ( + (-p11))*x2*x4*x5*x6 + ( + (-p11))*x5*x6 + ( + (-p11))*x4*x6 + ( + (-p11))*x2^2*x3*x4*x5*x6 + ( + (-p11))*x2*x3*x5*x6 + ( + (-p11))*x2*x3*x4*x6 + ( + (-p11))*x2*x5*x6 + ( + (-p11))*x6 + ( + (-p11))*x1*x2^2*x3*x4*x5*x6 + ( + (-p11))*x1*x2*x3*x5*x6 + ( + (-p11))*x1*x2*x3*x4*x6 + ( + (-p11))*x2*x4*x5 + ( + (-p11))*x5 + ( + (-p11))*x4 + ( + (-p11))*x1*x2^2*x3*x5*x6 + ( + (-p11))*x2^2*x3*x4*x5 + ( + (-p11))*x1*x2*x3*x6 + ( + (-p11))*x2*x3*x5 + ( + (-p11))*x2*x3*x4 + ( + (-p11))*x2*x5 + ( + (-p11));
  Id U(x1?,x2?,x3?,x4?,x5?,x6?,eps?) =  + ( + (1))*x1*x2*x4*x6 + ( + (1))*x2*x4*x5 + ( + (1))*x1*x6 + ( + (1))*x5 + ( + (1))*x4 + ( + (1))*x1*x2^2*x3*x4*x6 + ( + (1))*x2^2*x3*x4*x5 + ( + (1))*x1*x2*x3*x6 + ( + (1))*x2*x3*x5 + ( + (1))*x2*x3*x4 + ( + (1))*x1*x2*x6 + ( + (1))*x2*x5 + ( + (1)) + ( + (1))*x1^2*x2^2*x3*x4*x6 + ( + (1))*x1*x2^2*x3*x4*x5 + ( + (1))*x1^2*x2*x3*x6 + ( + (1))*x1*x2*x3*x5 + ( + (1))*x1*x2*x3*x4 + ( + (1))*x1*x2*x4 + ( + (1))*x1 + ( + (1))*x1^2*x2^2*x3*x6 + ( + (1))*x1*x2^2*x3*x5 + ( + (1))*x1*x2^2*x3*x4 + ( + (1))*x1*x2;

#endProcedure

* Define how deep functions to be inserted are nested.
#define insertionDepth "5"
