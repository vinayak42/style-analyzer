"""Javascript specific bablefish roles and internal types tooling."""


INTERNAL_TYPES_FREQ = {
    "Identifier":                   3.29693E-01,
    "MemberExpression":             1.11422E-01,
    "StringLiteral":                7.79709E-02,
    "CallExpression":               5.48868E-02,
    "NumericLiteral":               5.48544E-02,
    "ObjectProperty":               4.27282E-02,
    "ExpressionStatement":          3.82706E-02,
    "BlockStatement":               2.82340E-02,
    "BinaryExpression":             2.77853E-02,
    "AssignmentExpression":         2.66727E-02,
    "CommentLine":                  2.42488E-02,
    "VariableDeclarator":           2.26705E-02,
    "ThisExpression":               1.95187E-02,
    "VariableDeclaration":          1.40221E-02,
    "FunctionExpression":           1.28087E-02,
    "UnaryExpression":              1.21498E-02,
    "LogicalExpression":            1.19199E-02,
    "IfStatement":                  1.16962E-02,
    "ReturnStatement":              1.14007E-02,
    "ObjectExpression":             1.08154E-02,
    "ArrayExpression":              9.89254E-03,
    "CommentBlock":                 7.92774E-03,
    "BooleanLiteral":               4.60369E-03,
    "ConditionalExpression":        4.33093E-03,
    "SequenceExpression":           3.55159E-03,
    "NullLiteral":                  3.14558E-03,
    "FunctionDeclaration":          2.64378E-03,
    "NewExpression":                2.46833E-03,
    "UpdateExpression":             2.31793E-03,
    "RegExpLiteral":                1.85207E-03,
    "ForStatement":                 1.52464E-03,
    "SwitchCase":                   1.40751E-03,
    "Program":                      9.47163E-04,
    "File":                         9.46918E-04,
    "BreakStatement":               8.41647E-04,
    "ThrowStatement":               5.12712E-04,
    "JSXIdentifier":                5.10803E-04,
    "WhileStatement":               4.42731E-04,
    "ArrowFunctionExpression":      3.82068E-04,
    "ForInStatement":               3.80444E-04,
    "DirectiveLiteral":             3.65562E-04,
    "Directive":                    3.65504E-04,
    "TryStatement":                 3.25769E-04,
    "CatchClause":                  3.14035E-04,
    "ImportDeclaration":            2.50201E-04,
    "JSXAttribute":                 2.28075E-04,
    "JSXText":                      2.16715E-04,
    "GenericTypeAnnotation":        2.14377E-04,
    "SwitchStatement":              1.96378E-04,
    "TemplateElement":              1.85957E-04,
    "EmptyStatement":               1.78704E-04,
    "ContinueStatement":            1.71884E-04,
    "ImportSpecifier":              1.71205E-04,
    "JSXOpeningElement":            1.67299E-04,
    "JSXElement":                   1.67157E-04,
    "JSXExpressionContainer":       1.63536E-04,
    "TypeAnnotation":               1.49937E-04,
    "ClassMethod":                  1.47363E-04,
    "ImportDefaultSpecifier":       1.38596E-04,
    "JSXClosingElement":            1.08084E-04,
    "TemplateLiteral":              8.74693E-05,
    "TypeParameterInstantiation":   8.07660E-05,
    "ExportNamedDeclaration":       7.52456E-05,
    "ObjectTypeProperty":           6.78233E-05,
    "FunctionTypeParam":            6.52818E-05,
    "ObjectMethod":                 6.26104E-05,
    "DeclareModule":                6.10201E-05,
    "DeclareModuleExports":         6.07065E-05,
    "ObjectPattern":                5.31824E-05,
    "DoWhileStatement":             4.98662E-05,
    "AnyTypeAnnotation":            4.51962E-05,
    "ExportDefaultDeclaration":     4.45272E-05,
    "StringLiteralTypeAnnotation":  4.21846E-05,
    "FunctionTypeAnnotation":       4.18872E-05,
    "StringTypeAnnotation":         4.17763E-05,
    "ClassBody":                    3.54960E-05,
    "ClassDeclaration":             3.10996E-05,
    "NumberTypeAnnotation":         2.50202E-05,
    "AwaitExpression":              2.48789E-05,
    "ClassProperty":                2.47351E-05,
    "TypeParameter":                2.38582E-05,
    "ExportSpecifier":              2.33138E-05,
    "LabeledStatement":             2.32410E-05,
    "SpreadElement":                2.23778E-05,
    "AssignmentPattern":            2.23331E-05,
    "ObjectTypeAnnotation":         1.94508E-05,
    "BooleanTypeAnnotation":        1.44263E-05,
    "VoidTypeAnnotation":           1.41113E-05,
    "NullableTypeAnnotation":       1.32434E-05,
    "Super":                        1.30373E-05,
    "UnionTypeAnnotation":          1.21370E-05,
    "YieldExpression":              1.21280E-05,
    "TypeParameterDeclaration":     1.13776E-05,
    "JSXSpreadAttribute":           1.06881E-05,
    "ForOfStatement":               1.05943E-05,
    "TypeAlias":                    8.79370E-06,
    "ArrayPattern":                 8.70995E-06,
    "JSXMemberExpression":          7.20151E-06,
    "RestElement":                  6.31548E-06,
    "ImportNamespaceSpecifier":     6.10372E-06,
    "TaggedTemplateExpression":     5.60884E-06,
    "TypeCastExpression":           4.49440E-06,
    "ClassExpression":              4.41160E-06,
    "BigIntLiteral":                4.14703E-06,
    "WithStatement":                3.60218E-06,
    "ObjectTypeIndexer":            3.57173E-06,
    "ArrayTypeAnnotation":          3.49464E-06,
    "QualifiedTypeIdentifier":      3.43278E-06,
    "NumberLiteralTypeAnnotation":  3.31334E-06,
    "DeclareFunction":              3.10968E-06,
    "MixedTypeAnnotation":          2.43302E-06,
    "ExistsTypeAnnotation":         2.41827E-06,
    "TupleTypeAnnotation":          2.22317E-06,
    "DeclareTypeAlias":             2.11563E-06,
    "IntersectionTypeAnnotation":   2.06091E-06,
    "DebuggerStatement":            1.55936E-06,
    "ThisTypeAnnotation":           1.55603E-06,
    "TypeofTypeAnnotation":         1.48370E-06,
    "DeclareVariable":              1.40852E-06,
    "NullLiteralTypeAnnotation":    1.32096E-06,
    "DeclareClass":                 1.27908E-06,
    "DeclareExportDeclaration":     1.11492E-06,
    "ExportAllDeclaration":         1.08874E-06,
    "ObjectTypeCallProperty":       1.04877E-06,
    "InterfaceExtends":             9.94050E-07,
    "Decorator":                    9.27431E-07,
    "Variance":                     9.12204E-07,
    "Import":                       8.78419E-07,
    "InterfaceDeclaration":         8.40351E-07,
    "BooleanLiteralTypeAnnotation": 6.78562E-07,
    "JSXNamespacedName":            6.45252E-07,
    "JSXEmptyExpression":           5.58648E-07,
    "BindExpression":               3.12633E-07,
    "DeclareInterface":             2.08898E-07,
    "PrivateName":                  1.96050E-07,
    "MetaProperty":                 1.94623E-07,
    "ObjectTypeSpreadProperty":     1.73685E-07,
    "ClassImplements":              1.59886E-07,
    "EmptyTypeAnnotation":          9.23149E-08,
    "ClassPrivateProperty":         7.42326E-08,
    "JSXClosingFragment":           6.47156E-08,
    "JSXFragment":                  6.47156E-08,
    "JSXOpeningFragment":           6.47156E-08,
    "InferredPredicate":            3.61646E-08,
    "DoExpression":                 3.09302E-08,
    "OpaqueType":                   2.52200E-08,
    "DeclareOpaqueType":            1.95098E-08,
    "DeclaredPredicate":            1.23721E-08,
    "ClassPrivateMethod":           9.04115E-09,
    "JSXSpreadChild":               6.66190E-09,
    "DeclareExportAllDeclaration":  5.71020E-09,
}

ROLES_FREQ = {
    "EXPRESSION":                   2.27220E-01,
    "IDENTIFIER":                   1.31607E-01,
    "BINARY":                       5.23597E-02,
    "CALL":                         5.21110E-02,
    "LITERAL":                      4.81133E-02,
    "MAP":                          3.99017E-02,
    "QUALIFIED":                    3.30707E-02,
    "STATEMENT":                    3.26387E-02,
    "ARGUMENT":                     2.67647E-02,
    "OPERATOR":                     2.37406E-02,
    "ASSIGNMENT":                   2.33364E-02,
    "STRING":                       2.30914E-02,
    "LEFT":                         1.94902E-02,
    "RIGHT":                        1.94860E-02,
    "NUMBER":                       1.62260E-02,
    "CALLEE":                       1.61835E-02,
    "FUNCTION":                     1.59193E-02,
    "IF":                           1.56945E-02,
    "DECLARATION":                  1.55777E-02,
    "KEY":                          1.26829E-02,
    "VALUE":                        1.26813E-02,
    "BOOLEAN":                      1.20834E-02,
    "BODY":                         1.17311E-02,
    "INITIALIZATION":               1.15169E-02,
    "VARIABLE":                     1.07869E-02,
    "BLOCK":                        1.06369E-02,
    "COMMENT":                      9.45669E-03,
    "SCOPE":                        8.31112E-03,
    "THIS":                         5.74089E-03,
    "CONDITION":                    5.73547E-03,
    "ARITHMETIC":                   5.68724E-03,
    "THEN":                         4.70618E-03,
    "UNARY":                        4.26266E-03,
    "RELATIONAL":                   3.96160E-03,
    "LIST":                         3.95746E-03,
    "RETURN":                       3.35335E-03,
    "ADD":                          2.84460E-03,
    "NOT":                          2.43363E-03,
    "AND":                          2.15163E-03,
    "FOR":                          2.14602E-03,
    "ELSE":                         2.05036E-03,
    "IDENTICAL":                    1.73029E-03,
    "OR":                           1.50575E-03,
    "NEGATIVE":                     1.29969E-03,
    "INCOMPLETE":                   1.22355E-03,
    "EQUAL":                        1.07635E-03,
    "NULL":                         1.01586E-03,
    "NAME":                         9.55249E-04,
    "CASE":                         7.99685E-04,
    "UNANNOTATED":                  7.61483E-04,
    "SUBSTRACT":                    6.43246E-04,
    "LESS_THAN":                    5.62905E-04,
    "POSTFIX":                      5.47646E-04,
    "REGEXP":                       5.44053E-04,
    "SWITCH":                       5.28540E-04,
    "TYPE":                         5.16952E-04,
    "MULTIPLY":                     3.98252E-04,
    "UPDATE":                       3.91794E-04,
    "WHILE":                        3.89548E-04,
    "IMPORT":                       3.83130E-04,
    "GREATER_THAN":                 3.69933E-04,
    "MODULE":                       3.13476E-04,
    "BITWISE":                      3.02535E-04,
    "FILE":                         2.78004E-04,
    "BREAK":                        2.47014E-04,
    "ITERATOR":                     2.29536E-04,
    "DIVIDE":                       2.24338E-04,
    "TRY":                          1.93855E-04,
    "THROW":                        1.50473E-04,
    "GREATER_THAN_OR_EQUAL":        1.36234E-04,
    "INCREMENT":                    1.06784E-04,
    "CATCH":                        9.21710E-05,
    "LESS_THAN_OR_EQUAL":           8.87912E-05,
    "PATHNAME":                     7.61687E-05,
    "RIGHT_SHIFT":                  6.86756E-05,
    "MODULO":                       6.62360E-05,
    "POSITIVE":                     5.84406E-05,
    "CONTINUE":                     5.04448E-05,
    "DO_WHILE":                     4.38977E-05,
    "LEFT_SHIFT":                   4.19807E-05,
    "UNSIGNED":                     3.96714E-05,
    "VISIBILITY":                   3.55279E-05,
    "DECREMENT":                    2.61355E-05,
    "XOR":                          1.71866E-05,
    "BASE":                         9.72369E-06,
    "FINALLY":                      6.07444E-06,
    "ARGS_LIST":                    2.48357E-06,
    "INSTANCE":                     5.75366E-08,
}

INTERNAL_TYPES = sorted(INTERNAL_TYPES_FREQ)
INTERNAL_TYPES_INDEX = {r:  i for i, r in enumerate(INTERNAL_TYPES)}
ROLES = sorted(ROLES_FREQ)
ROLES_INDEX = {r:  i for i, r in enumerate(ROLES)}
