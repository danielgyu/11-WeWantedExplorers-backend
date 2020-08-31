# SECURITY WARNING: keep the secret key used in production secret!
SECRET = {
    'secret' = 'lep=@*wro0wj&mel=tn8!*o7l2%ojwcj1b36j3hei=!tt$5=x%',
}

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wwe',
        'USER': 'mayfly',
        'PASSWORD': 'daniel92',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'TEST': {
            'NAME': 'test_wwe',
        }
    }
}
