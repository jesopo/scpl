# scpl
simple compact pattern language

```
✨ ~/src/jess/scpl main % python3 -m scpl.eval 'true && a' '{"a": "false"}'
tokens  : [Word(true), Space( ), Operator(&&), Space( ), Word(a)]
ast     : And(Bool(true), Variable(a))
constant: False
precomp : And(Bool(true), Variable(a))
vars    : {'a': Bool(false)}
eval    : Bool(false)
duration: 9.92μs
```
