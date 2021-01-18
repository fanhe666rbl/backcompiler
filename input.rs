// "this"
// "this is not     a comment"
// 1 + 2 + 3.5
const k: int = 0;
let t: int = 0;

fn fib(x: int) -> int {
    // 1 + 2 * fib(11);
    let i : int = 0;
    if x<=1 {
       return 1;
    }
    let result: int = fib(x - 1);
    result = result + fib(x - 2);
    // x = 1+(2*3)-6 as int +(2+2)-i /( fib(i)*(1+3)+5);
    // 1+(2*3)-6 as int +(2+2)-i /( fib(i)*(1+3)+5);
    return result;
}

fn main() -> int {
    let i: int = 0;
    let j: int = 10;
    // j = getint();
    while i < j {
        // putint(i);
        // putchar(32);
        // putint(fib(i));
        // putln();
        i = i + 1;
    }
    return 0;
}