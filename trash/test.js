function debounce(wait, func) {
    let can_run = true;
    let timeout = 0;

    function res(args) {
        setTimeout(
            () => {
                if (wait > timeout) {
                    // func(args)
                    // tim
                    // ...
                }
            },
            wait
        );

    }
}

const lazyShowMessage = debounce(100, console.info)

lazyShowMessage('1 not showed')
lazyShowMessage('2 showed')
// => 2 showed

setTimeout(lazyShowMessage, 200, '3 not showed')
// =>

setTimeout(() => {
    lazyShowMessage('4 not showed')
    lazyShowMessage('5 showed')
}, 210)

setTimeout(() => {
    let deinit
    deinit = lazyShowMessage('6 not showed')
    deinit = lazyShowMessage('7 not showed')
    if (deinit) deinit()
}, 400)