# -*- encoding: utf-8 -*-


class BaseScope:
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        # 运算符重载
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))  # 去重

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))  # 去重

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))  # 去重

        return self


class UserScope(BaseScope):
    # allow_api = ['v1.user+get_user', 'v1.user+delete_user']
    forbidden = ['v1.user+super_get_user', 'v1.user+super_delete_user']
    allow_module = ['v1.gift']

    def __init__(self):
        self + AdminScope()


class AdminScope(BaseScope):
    # allow_api = ['v1.user+super_get_user', 'v1.user+super_delete_user']
    allow_module = ['v1.user', 'v1.gift']

    def __init__(self):
        pass
        # self + UserScope()


def is_in_scope(scope, endpoint):
    # v1.view_func   v1.module_name+view_func -> v1.redprint_name+view_func
    scope = globals().get(scope, None)()
    module_name, view_func = endpoint.split('+')
    if endpoint in scope.forbidden:
        return False
    if module_name in scope.allow_module:
        return True
    if endpoint in scope.allow_api:
        return True
    return False


# if __name__ == '__main__':
    # print(SuperScope().__dict__)
