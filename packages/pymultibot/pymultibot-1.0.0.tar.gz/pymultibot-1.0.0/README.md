# pymultibot

Unofficial python library to use service of multibot.in

## Python support
Pymultibot support python 3.8+

## Installing pymultibot

```
$ python -m pip install pymultibot
```

## How to use

### Result

when using the pymultibot method will return a tupple data type.

Example

```
(True,token_solution)
(False,error)
```

The first index has a bool data type and the second index has a string data type. If the value of the first index is True then the value of the second index is the token/solution answer of the captcha, if the value of the first index is False then the value of the second index is an error message.

### Init pymultibot

```
from pymultibot import Multibot

multibot_apikey = "xxxxxx"
mb = Multibot(multibot_apikey)
```

### Get balance

```
status,balance = mb.get_balance()
print(balance)
```

Result

Total available token multibot
```
1000
```

### Google recaptcha v2

```
siteurl = "https://google.com/recaptcha/api2/demo"
sitekey = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-

status,token = mb.recaptchav2(sitekey,siteurl)
print(token)
```

Result

Token google recaptcha v2 solution
```
03AFcWeA6UK0iTBbetdQp_TwhpgLjm4f-j....
```
### Hcaptcha

```
siteurl = "https://accounts.hcaptcha.com/demo"
sitekey = "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2"

status,token = mb.hcaptcha(sitekey,siteurl)
print(token)
```

Result

Token hcaptcha solution
```
P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.....
```
### Image captcha

```
from base64 import b64encode

image = "captcha_example/image_captcha.jpg" 
read_image = open(image,'rb').read()
image_base64 = b64encode(read_image).decode('utf-8')
status,solve = mb.image_ocr(image_base64)
print(solve)
```

Result

Text from image
```
rbskw
```

### Upside down

```
image = "captcha_example/upside_down.png"
read_image = open(image,'rb').read()
image_base64 = b64encode(read_image).decode('utf-8')
status,solve = mb.upside_down(image_base64)
print(solve)
```

Result

coordinates of the object facing downwards

```
264:55
```

### RsCaptcha / IonCaptcha

```
image = "captcha_example/rscaptcha.png"
read_image = open(image,'rb').read()
image_base64 = b64encode(read_image).decode('utf-8')
status,solve = mb.rscaptcha(image_base64)
print(solve)
```

Result

Coortinates for the click

```
79:28
```

### Antibotlinks


HTML
```
<p class="alert alert-warning text-center">Please click on the Anti-Bot links in the following order <img src="data:image/png;base64,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" alt width="130" height="24" /> <a href="#" id="antibotlinks_reset">( reset )</a></p>

<script type="text/javascript"> var ablinks = ["<a href=\"#\" rel=\"7603\"><img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAoCAYAAAACJPERAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAB7klEQVRYhe2XsUodQRSGP8NFJAwSNAQRYeYBxCKFSmISUFshYBGIoOADpMkTWKbwAawE8wKBkLQKkQRFxMLSYgYkiFhImEokWOxZOLns7Nx7E7m5MT8se/bMzPlmzu6Z3YW/Uc7Yva6AqsC3Mpm6oF1b/b8H7ERdm2RPZKd7ypTMsjN2tNPYfSmgj2GqBvoJuA8s+Ri+O2PHgLeAAQaBdz6Gw9T4e1XODHAAeCDQ5+KeB54AE8AIcJwan4QqQFWKJ4CG2D/k/FS1H/oYrjqG+himKsCTyj5wxg4Cr5XvS13MLLQEl7Yzth9YkMt9H8M5MEORznHxf/1taJNeUtzPa2BdfM/kfAyc+BjO/hhUVrkklxs+Bu+MbQDTqls2tW1BKe7bCLDrY9gS32OKp7jUrppkss5bgjpjh4AV4AxYU00zyr5ESiVX541UQ5NWKVZ0Drxxxl4CF8AL1eeIYhE/64CQ2JG0nLEGeA88BPoz3U99DIu5mEloVYpkAkNyvAJmpemKolS++Rg+5OLUKrPpbzpj9+RYT/WripNNbyLII+Cjcq35GD63Or7dzaHUrLKvUaVym9A5ZR/5GMqNv6XPlLahUrPjyrWt2xMviV/Uap1qDQAbFHvwMLDT3KGtp/Vuqyc/nHvjH6g3Zvlfd1Y3h8yT7l53lS0AAAAASUVORK5CYII=\" alt=\"\" width=\"29\" height=\"40\" style=\"border:1px solid #222222;border-radius:5px;margin:2px;\" /></a>", "<a href=\"#\" rel=\"5279\"><img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABoAAAAoCAYAAADg+OpoAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABWklEQVRYhe2WsS8EQRTGf46IKGRLUVyGhtC4foqNilanUCkV/gyVQsSfoJSIQoVMMQlRKHQUbhyJKy5yUW5EFDuSdfZyL3dus3f26+bte+978823OwsFCvwlQq3uh4Nk8JCpLMN5BoWEfUWnHY8IGywBu4ACHoEr4MxYF33nGOvmeyLyjapA1BJ+B7aMdXeSHiVJkrFuFtgEDoG6D08BC20G+yWjiMijAVSAab++Bk7SSNJklEo3BxwDkz50DuwY6z6kU0p3NA6MJdbPwKeUBGBUkuRqzYYqBxfAIrF0FWBdlYOqqzWfJD3EZ2SsewCWgW1ix80AB6FWQVdEaY4JtVoJtXoF1oBL4Mg/mgDKEqJUMySdE2q1Cuy3qb8FNox1HYlSpWux5w1wys8X9g3Yk5KA0N4AoVYl4k9QZKx7kdYNDpKm6ftdlSlZLpCvX+V8TdNjTdf4H87LHF89h22v1TiiKAAAAABJRU5ErkJggg==\" alt=\"\" width=\"26\" height=\"40\" style=\"border:1px solid #222222;border-radius:5px;margin:2px;\" /></a>", "<a href=\"#\" rel=\"4415\"><img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABoAAAAoCAYAAADg+OpoAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABmklEQVRYhe2WvUoDQRSFP8U/gohFtNNWsRiQLOIDqFhM40Poa6Sw9Sl8AsGtrHyAKXQqBVFsxMJCREJIRCx2RmfDJntjNjGRHFj2zs/eM+fes+zCX0HpqFnkvkIe7ons/2Og5RnKXgzkUEOpvG+YkGxSOloAboGau+rh3cbmIC/HlPBA80C5zVpDkmBSSDQXxCdABTh041qRRKUgfrSxscBdN0TS0oWKfOIrYBf4/BWR0lHTxma6ZTpU1ACwsXkHLoUHTbuuDQlKR/vAuRu+AM8kygxQtbF5zSNKKcoicQhLV+bHgVvAKpBrb6kZzoAlYAVYAzaBC7e2I0kgMoONDUCqPEpHFtijgxnCVkgVZcGXs+6TZpH4eZEipaMjoOqSVlzzPVENkv6GClrH0vdoEVh28Ye7e8vX/aZWM4VjaelmgtgnTinKg5Ro1gc2Nl5RV0TS0j34QOnoGngD1t3UfbCW+cKDXNEpELt4A9gm6dsTcJxHAsIPn4fSkTdFicQUN0EpxxhRjH8ov1H4KTsl9Gs9k0oSjEb9+4kvS0WVCiF7NsMAAAAASUVORK5CYII=\" alt=\"\" width=\"26\" height=\"40\" style=\"border:1px solid #222222;border-radius:5px;margin:2px;\" /></a>"]</script>
```

Python code get parameter !

```
data = {}
parser = bs(html,'html.parser')
main = parser.find('p').find('img').get('src').replace('data:image/png;base64,','')
ablinks = re.findall(r'<a href=\"#\" rel=\"(.*?)\"><img src=\"(.*?)\"',html)
data['main'] = main
for ab in ablinks:
    key,value = ab
    data[key] = value.replace('data:image/png;base64,','')

print(data)
```

Result variable data

```
{
    'main': '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',
    '7603': 'iVBORw0KGgoAAAANSUhEUgAAAB0AAAAoCAYAAAACJPERAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAB7klEQVRYhe2XsUodQRSGP8NFJAwSNAQRYeYBxCKFSmISUFshYBGIoOADpMkTWKbwAawE8wKBkLQKkQRFxMLSYgYkiFhImEokWOxZOLns7Nx7E7m5MT8se/bMzPlmzu6Z3YW/Uc7Yva6AqsC3Mpm6oF1b/b8H7ERdm2RPZKd7ypTMsjN2tNPYfSmgj2GqBvoJuA8s+Ri+O2PHgLeAAQaBdz6Gw9T4e1XODHAAeCDQ5+KeB54AE8AIcJwan4QqQFWKJ4CG2D/k/FS1H/oYrjqG+himKsCTyj5wxg4Cr5XvS13MLLQEl7Yzth9YkMt9H8M5MEORznHxf/1taJNeUtzPa2BdfM/kfAyc+BjO/hhUVrkklxs+Bu+MbQDTqls2tW1BKe7bCLDrY9gS32OKp7jUrppkss5bgjpjh4AV4AxYU00zyr5ESiVX541UQ5NWKVZ0Drxxxl4CF8AL1eeIYhE/64CQ2JG0nLEGeA88BPoz3U99DIu5mEloVYpkAkNyvAJmpemKolS++Rg+5OLUKrPpbzpj9+RYT/WripNNbyLII+Cjcq35GD63Or7dzaHUrLKvUaVym9A5ZR/5GMqNv6XPlLahUrPjyrWt2xMviV/Uap1qDQAbFHvwMLDT3KGtp/Vuqyc/nHvjH6g3Zvlfd1Y3h8yT7l53lS0AAAAASUVORK5CYII=',
    '5279': 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAoCAYAAADg+OpoAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABWklEQVRYhe2WsS8EQRTGf46IKGRLUVyGhtC4foqNilanUCkV/gyVQsSfoJSIQoVMMQlRKHQUbhyJKy5yUW5EFDuSdfZyL3dus3f26+bte+978823OwsFCvwlQq3uh4Nk8JCpLMN5BoWEfUWnHY8IGywBu4ACHoEr4MxYF33nGOvmeyLyjapA1BJ+B7aMdXeSHiVJkrFuFtgEDoG6D08BC20G+yWjiMijAVSAab++Bk7SSNJklEo3BxwDkz50DuwY6z6kU0p3NA6MJdbPwKeUBGBUkuRqzYYqBxfAIrF0FWBdlYOqqzWfJD3EZ2SsewCWgW1ix80AB6FWQVdEaY4JtVoJtXoF1oBL4Mg/mgDKEqJUMySdE2q1Cuy3qb8FNox1HYlSpWux5w1wys8X9g3Yk5KA0N4AoVYl4k9QZKx7kdYNDpKm6ftdlSlZLpCvX+V8TdNjTdf4H87LHF89h22v1TiiKAAAAABJRU5ErkJggg=='
    '4415': 'iVBORw0KGgoAAAANSUhEUgAAABoAAAAoCAYAAADg+OpoAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABmklEQVRYhe2WvUoDQRSFP8U/gohFtNNWsRiQLOIDqFhM40Poa6Sw9Sl8AsGtrHyAKXQqBVFsxMJCREJIRCx2RmfDJntjNjGRHFj2zs/eM+fes+zCX0HpqFnkvkIe7ons/2Og5RnKXgzkUEOpvG+YkGxSOloAboGau+rh3cbmIC/HlPBA80C5zVpDkmBSSDQXxCdABTh041qRRKUgfrSxscBdN0TS0oWKfOIrYBf4/BWR0lHTxma6ZTpU1ACwsXkHLoUHTbuuDQlKR/vAuRu+AM8kygxQtbF5zSNKKcoicQhLV+bHgVvAKpBrb6kZzoAlYAVYAzaBC7e2I0kgMoONDUCqPEpHFtijgxnCVkgVZcGXs+6TZpH4eZEipaMjoOqSVlzzPVENkv6GClrH0vdoEVh28Ye7e8vX/aZWM4VjaelmgtgnTinKg5Ro1gc2Nl5RV0TS0j34QOnoGngD1t3UfbCW+cKDXNEpELt4A9gm6dsTcJxHAsIPn4fSkTdFicQUN0EpxxhRjH8ov1H4KTsl9Gs9k0oSjEb9+4kvS0WVCiF7NsMAAAAASUVORK5CYII='
}
```

Python code to get captcha result 

```
status, solve = mb.anti_bot(data)
print(solve)
```

Result

```
5279,4415,7603
```