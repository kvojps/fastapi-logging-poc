from api.models.user_log import Area, Type

METHOD_MAPPING = {
    "POST": (Type.CRIACAO, {
        "users": Area.USUARIOS
    }),
    "PUT": (Type.EDICAO, {
        "users": Area.USUARIOS
    }),
    "PATCH": (Type.EDICAO, {
        "users": Area.USUARIOS
    }),
    "DELETE": (Type.EXCLUSAO, {
        "users": Area.USUARIOS
    })
}
