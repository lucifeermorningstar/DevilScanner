from Sibyl_System import system_cmd, System
from PIL import Image
import os

@System.on(system_cmd(pattern = r'get_id'))
async def image_maker(event) -> None:
 replied_user = await event.get_reply_message()
 await System.download_profile_photo(replied_user.from_id, file= 'user.png', download_big = True)
 user_photo = Image.open('user.png')
 id_template = Image.open('ID.png')
 user_photo = user_photo.resize((123, 134))
 id_template.paste(user_photo, (146, 66))
 id_template.save('user_id.png')
 await System.send_message(
        event.chat_id,
        "Generated User Profile Photo",
        reply_to=event.message.id,
        file='user_id.png',
        force_document=False,
        silent=True
    )
 
 
