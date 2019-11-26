mod print;

fn vars_test() {
    let name = "dimitrius";
    let mut age = 25;
    println!("I am {} and i'm {}", name, age);  // to avoid warning
    age = 26;
    println!("I am {} and i'm {}", name, age);

    asd = 13;
}

fn main() {
    print::run();
    println!("Hello, world!");
    vars_test();
}
