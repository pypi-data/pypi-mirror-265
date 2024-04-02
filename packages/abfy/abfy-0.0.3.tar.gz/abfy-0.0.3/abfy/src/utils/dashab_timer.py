def time_profiler(process_name):
    def inner_time_function(func):
        def wrapper(*args, **kwargs):
            timer_callback = kwargs.get("timer_callback")
            if timer_callback:
                with timer_callback(process_name):
                    response = func(*args, **kwargs)
            else:
                response = func(*args, **kwargs)
            return response

        return wrapper

    return inner_time_function
