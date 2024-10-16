import requests


def postagem(page_id, access_token, photo_path, message,publicacao):
    # Endpoint para upload da foto
    upload_url = f'https://graph.facebook.com/{page_id}/photos'

    # POST A SER ENVIADO
    print(" \n POSTAGEM SENDO ENVIADA:", "\n PAGE_ID: " + page_id, "\n TOKEN: " + access_token, "\n PATH: " + photo_path, "\n MENSAGEM: " + message + "\n")
    
    try:
        with open(photo_path, 'rb') as photo_file:
            response = requests.post(upload_url,
                                     params={'access_token': access_token},
                                     files={'source': photo_file},
                                     data={'message': message})

            upload_result = response.json()

        # Verificar se o upload foi bem-sucedido
        if 'id' in upload_result:
            photo_id = upload_result['id']
            print(f'Foto enviada com sucesso. ID da foto: {photo_id}')
            if publicacao.post_id:
                publicacao.post_id += f',{photo_id}'  # Concatena o novo ID ao existente
            else:
                publicacao.post_id = photo_id  # Se for o primeiro ID, apenas atribui
            publicacao.save()
            return True 
        else:
            print(f'Erro ao enviar foto: {upload_result}')
            return False  # Retorna False se ocorreu um erro no upload

    except Exception as e:
        print(f"Ocorreu um erro ao tentar enviar a foto: {e}")
        return False  
    
def postagem_video(page_id, access_token, file_name, file_path, file_length, file_type, message, app_id,publicacao):
    # Endpoint para upload do vídeo
    upload_url = f'https://graph.facebook.com/{page_id}/videos'
    
    # POST A SER ENVIADO
    print(" \n POSTAGEM DE VÍDEO SENDO ENVIADO:", "\n PAGE_ID: " + page_id, "\n TOKEN: " + access_token, "\n PATH: " + file_path, "\n MENSAGEM: " + message, "\n APP_ID: " + app_id + "\n")

    try:
        with open(file_path, 'rb') as video_file:
            response = requests.post(upload_url,
                                     params={'access_token': access_token, 'app_id': app_id},
                                     files={'source': (file_name, video_file, file_type)},
                                     data={
                                         'description': message,
                                         'file_size': file_length
                                     })

            upload_result = response.json()

        # Verificar se o upload foi bem-sucedido
        if 'id' in upload_result:
            video_id = upload_result['id']
            print(f'Vídeo enviado com sucesso. ID do vídeo: {video_id}')
            if publicacao.post_id:
                publicacao.post_id += f',{video_id}'  # Concatena o novo ID ao existente
            else:
                publicacao.post_id = video_id  # Se for o primeiro ID, apenas atribui
            publicacao.save()
            return True  # Retorna True se a postagem foi bem-sucedida
        else:
            print(f'Erro ao enviar vídeo: {upload_result}')
            return False  # Retorna False se ocorreu um erro no upload

    except Exception as e:
        print(f"Ocorreu um erro ao tentar enviar o vídeo: {e}")
        return False


