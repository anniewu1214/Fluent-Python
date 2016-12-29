import time

registry = set()


def register(active=True):
    def decorate(func):
        print('running register(active=%s)->decorate(%s)' % (active, func))
        if active:
            registry.add(func)
        else:
            registry.discard(func)

        return func

    return decorate


@register(active=False)
def f1():
    print('running f1()')


@register()
def f2():
    print('running f2()')


def f3():
    print('running f3()')


def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()


DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


# parameterized clock decorator
def clock_param(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            # using **locals() allows any local variable of
            # clocked to be referenced in the fmt
            print(fmt.format(**locals()))
            return _result

        return clocked

    return decorate


def clock_para_run():
    @clock_param('{name}: {elapsed}s')
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)


if __name__ == '__main__':
    main()
    clock_para_run()
