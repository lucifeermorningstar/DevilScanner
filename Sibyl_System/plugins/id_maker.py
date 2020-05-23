from Sibyl_System import system_cmd, System
from PIL import Image, ImageDraw, ImageFont
import os

@System.on(system_cmd(pattern = r'get_id'))
async def image_maker(event) -> None:
 replied_user = await event.get_reply_message()
 #Download profile photo
 await System.download_profile_photo(replied_user.from_id, file= 'user.png', download_big = True)
 user_photo = Image.open('user.png')
 #open id photo
 id_template = Image.open('ID.png')
 #resize user photo to fit box in id template
 user_photo = user_photo.resize((989, 1073))
 #put image in position
 id_template.paste(user_photo, (1229, 573))
 #postion on where to draw text
 position = (2473, 481)
 draw = ImageDraw.Draw(id_template)
 color = 'rgb(23, 43, 226)' #blue-ish color
 font = ImageFont.truetype('Sibyl_System/plugins/arial-unicode-ms.ttf', size=200)
 #put text in image
 draw.text(position, replied_user.sender.first_name.replace('\u2060', ''), fill=color, font=font)
 id_template.save('user_id.png')
 await System.send_message(
        event.chat_id,
        "Generated User ID",
        reply_to=event.message.id,
        file='user_id.png',
        force_document=True,
        silent=True
    )
