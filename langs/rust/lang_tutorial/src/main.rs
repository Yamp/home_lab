fn main() {
    str_inter_test();
    const_test();
    arr_test();
    tup_test();
    iter_test();
}

fn str_inter_test() {
    let age = 26;
    println!("I'm {} y.o.", age)
}

fn const_test() {
    const MY_PI: f32 = 3.1323423;
    println!("pi: {}", MY_PI)
}

fn arr_test() {
    let a: [i32; 5] = [1, 2, 3, 4, 5];
    println!("{}", a[3])
}

fn tup_test() {
    let a = (1, 1.2, "asd");
    let (_x, _y, z) = a;
    println!("{}", z)
}

fn iter_test() {
    let a = [12, 4, 6, 34, 5, 8, 45, 76, 76];
    for i in a.iter() {
        print!("{} ", i)
    }
    println!();
}
