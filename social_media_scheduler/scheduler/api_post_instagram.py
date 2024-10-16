import requests



def postar_no_instagram(image_url, caption, access_token, ig_user_id, publicacao):
    
    try:
        # Etapa 1: Criar o contêiner de mídia
        media_endpoint = f"https://graph.instagram.com/v20.0/{ig_user_id}/media"
        media_payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token
        }

        media_response = requests.post(media_endpoint, json=media_payload)
        media_data = media_response.json()

        if "id" not in media_data:
            return False, f"Erro ao criar contêiner de mídia: {media_data}"

        creation_id = media_data["id"]
        print(f"Contêiner de mídia criado com sucesso. ID: {creation_id}")

        # Etapa 2: Publicar o contêiner de mídia
        publish_endpoint = f"https://graph.instagram.com/v20.0/{ig_user_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": access_token
        }

        publish_response = requests.post(publish_endpoint, json=publish_payload)
        publish_data = publish_response.json()

        if "id" not in publish_data:
            return False, f"Erro ao publicar contêiner de mídia: {publish_data}"

        publish_id = publish_data["id"]
        print(f"Publicação realizada com sucesso. ID de mídia: {publish_id}")

        # Armazena o ID da postagem no objeto publicacao
        if publicacao.post_id:
            publicacao.post_id += f',{publish_id}'  # Concatena o novo ID ao existente
        else:
            publicacao.post_id = publish_id  # Se for o primeiro ID, apenas atribui
        
        publicacao.save()  # Salva as alterações no banco de dados

        return True, "Postagem realizada com sucesso."

    except Exception as e:
        return False, str(e)
