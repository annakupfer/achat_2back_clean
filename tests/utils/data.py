TEST_PHONE = "9859698002"
CALLER_PHONE = "9859698002"
CALLEE_PHONE = "9012345678"
CONTACT_PHONE = "9909898908"
OTP_CODE = "00000"
TEST_PARTICIPANT_ID = 38
TEST_ADD_CONTACT_ID = 1
TEST_CHAT_ID = 145

WS_SEND_MESSAGE_TO_USER_PAYLOAD = {
  "action":"send_message",
  "participant_id": TEST_PARTICIPANT_ID,
  "message":"hi, user 3",
  "documents":[
   # {
    #  "name":"file2.png",
    #  "type":"image/png",
    #  "url":"uploads/d964c2be-89b0-4f9e-9da4-eec99ad094a4_file2.png"
    #}
  ]
}
WS_SEND_MESSAGE_TO_GROUP_PAYLOAD = {
  "action":"send_message",
  "chat_id": TEST_CHAT_ID,
  "message":"hi, user 3",
  "documents":[
   # {
    #  "name":"file2.png",
    #  "type":"image/png",
    #  "url":"uploads/d964c2be-89b0-4f9e-9da4-eec99ad094a4_file2.png"
    #}
  ]
}

EXPECTED_CHAT_MESSAGE_NO_ATTACHMENTS = {
  "type": "chat_message",
  "messages": {
    "id": 3202,
    "message": "Текст",
    "sender": 184,
    "created": "2025-07-09T21:55:47",
    "isMyMessage": True,
    "isRead": False,
    "isForwarded": False,
    "type": "OTHER",
    "attachments": [
    #  {
    #   "id": 343,
    #    "url": "uploads/d964c2be-89b0-4f9e-9da4-eec99ad094a4_Видосик.mp4",
    #    "name": "Видосик.mp4",
    #    "type": "video/mp4",
    #    "thumbnail": "https://api.jv.test.messenger.akatosphere.ru/s3/media-bucket/uploads/thumbnails/d508b23f...b9d5a",
    #    "duration": "2"
    #  }
    ]
  },
  "chat_id": 200,
  "original_sender": "19",
  "original_message_id": None,
  "is_reply": False
}
EXPECTED_CONFIRMATION = {
    "type": "confirmation",
    "message": "Message successfully",
    "created": True,
    "chat_id": 0
}

headers = {"Content-Type": "application/json",
           "Accept": "*/*",
           "User-Agent": "PostmanRuntime/7.48.0"}

def headers_with_token(token):
    return{
        "Content-Type": "application/json", 
        "Accept": "*/*",
        "Authorization": f"Bearer {token}"
    }
WS_REPLY_PAYLOAD_TEMPLATE = {
   "action":"reply_message",
   "chat_id": None,
   "original_message_id": None,
   "reply_text":"ответ",
   "attachments":[
      #{
      #  "name":"attachments.mp4",
      #  "type": "video/mp4",
      #  "url":"uploads/d964c2be-89b0-4f9e-9da4-eec99ad094a4_Видосик.mp4"
      #}
   ]
}
EXPECTED_REPLY_MESSAGE = {
   "type": "chat_message",
   "messages": {
      "id": 3291,
      "message": "ответ",
      "sender": 13,
      "created": "2025-07-21T12:54:52",
      "isMyMessage": False,
      "isRead": False,
      "isForwarded": False,
      "type": "TEXT",
      "attachments": []
   },
   "chat_id": 219,
   "original_sender": None,
   "original_message_id": 3290,
   "is_reply": True
}
WS_GET_CHATS_PAYLOAD = {
  "action": "get_chats" 
}
EXPECTED_CHAT_LIST_STRUCTURE = EXPECTED_CHAT_LIST_STRUCTURE = {
    "type": str,
    "chats": [
        {
            "id": int,
            "chatName": str,
            "isPublic": bool,
            "lastName": (str, type(None)),
            "description": (str, type(None)),
            "chatType": str,
            "created": str,
            "ownerId": int,
            "consist": bool,
            "avatar": (dict, type(None)),
            "onlineStatus": str,
            "unreadMessages": int,
            "manuallyUnread": bool,
            "lastMessage": (dict, type(None)),
            "participantId": list,  # теперь это список ID, а не [0]
            "isPinned": bool,
            "notificationsEnabled": bool,
            "draft": (dict, type(None)),
            "invitationLink": (dict, type(None))  # новое поле
        }
    ]
}
WS_GET_MESSAGES_TEMPLATE = {
  "action": "get_messages",
  "chat_id": None,
  "page_number": "0"
}
EXPECTED_MESSAGE_STRUCTURE = {
    "type": str,
    "messagesList": [
        {
            "date": str,
            "messagesInDate": [
                {
                    "id": int,
                    "message": str,
                    "sender": int,
                    "created": str,
                    "isMyMessage": bool,
                    "isRead": bool,
                    "isForwarded": bool,
                    "type": str,
                    "attachments": [
                        {
                            "id": int,
                            "url": str,
                            "name": str,
                            "type": str,
                            "thumbnail": str,
                            "duration": (str, type(None))  # может быть строкой или None
                        }
                    ]
                }
            ]
        }
    ] 
}
WS_GET_CHAT_INFO_TEMPLATE = {
  "action": "get_chat",
  "chat_id": None
}
WS_CALL_INITIATION_PAYLOAD = {
   "action": "start_call",
   "callee_phone_number": "9000000002",
  
   "sdp": "sdp-данные"   
}
EXPECTED_CALL_STARTED_RESPONSE = {
   "type": "call_started",
   "call_id": (int, type(None)),
   "user_phone": "9000000001",
   "callee_phone": "9000000002",
   "sdp": "sdp-данные"   
}
EXPECTED_CALL_TIMED_OUT_RESPONSE = {
    "type": "call_timed_out",
    "call_id": 15,
    "user_phone": "9000000003",
    "callee_phone": "9000000002"
}
WS_FORWARD_MESSAGE_TO_GROUP_TEMPLATE =  {
    "action": "forward_message",
    "chat_id": None,
    "message": "Original message content",
    "attachments_message": [
        # Пример вложения (если нужно, можно раскомментировать и заполнить)
        # {
        #     "name": "file2.png",
        #     "type": "image/png",
        #     "url": "uploads/d964c2be-89b0-4f9e-9da4-eec99ad094a4_file2.png"
        # }
    ],
    "original_message_id": None
}
WS_FORWARD_MESSAGE_TO_USER_TEMPLATE = {
  "action": "forward_message",
  "participant_id": 38,
  "message": "пересылаю тебе это",
  "attachments_message": [],
  "forwarded_message": "Сообщение для Антонио без вложений",
  "attachments_forwarded_message": [],
  "original_message_id": None

}
EXPECTED_CHAT_CREATED_STRUCTURE = {
  "type": "chat_created",
  "chat_id": 200,
  "message": "You have been added to a new chat",
  "sender": 184
}
EXPECTED_FORWARDED_MESSAGE_STRUCTURE = {
  "type": "chat_message",
  "messages": {
    "id": 3206,
    "message": "This is a forwarded message",
    "sender": 184,
    "created": "2025-07-10T22:44:15",
    "isMyMessage": True,
    "isRead": False,
    "isForwarded": True,
    "type": "OTHER",
    "attachments": [
      #{
       # "id": 345,
       #"url": "uploads/d964c2be-89b0-4f9e-9da4-eec99ad094a4_Видосик.mp4",
       # "name": "Видосик.mp4",
       #"type": "video/mp4",
       # thumbnail": "https://api.jv.test.messenger.akatosphere.ru/s3/media-bucket/uploads/thumbnails/d508b23f...b9d5a",
       # "duration": "2"
      #}
    ]
  },
  "chat_id": 200,
  "original_sender": "184",
  "original_message_id": 81,
  "is_reply": False
}
WS_ADD_CONTACT_PAYLOAD = {
  "action": "add_contact",
  "contactPhone": CONTACT_PHONE
}
EXPECTED_CONFIRMATION_ADD_CONTACT = {
  "type": "contact_action",
  "action": "added",
  "timestamp": "2025-08-21 14:43:06.7664952",
  "contact_phones": [
    CONTACT_PHONE
  ]
}
WS_GET_CONTACTS_PAYLOAD = {
    "action": "get_contacts"
}
EXPECTED_CONTACTS_LIST = {
  "type": "contacts_list",
  "contacts": [
    {
      "idUser": 10,
      "idContact": 1,
      "phone": "9000000003",
      "firstName": "Test_first_name1",
      "lastName": "Test_last_name1",
      "createdAt": "2025-07-23 14:04:37",
      "onlineStatus": "2025-07-13T14:15:57.728106Z"
    },
    {
      "idUser": 11,
      "idContact": 2,
      "phone": "9000000002",
      "firstName": "Test_first_name2",
      "lastName": "Test_last_name2",
      "createdAt": "2025-07-23 14:04:42",
      "onlineStatus": "2025-07-13T14:15:57.728106Z"
    }
  ]
}
USER_UPDATEDATA_PAYLOAD = {
  "firstName": "testUser",
  "lastName": "",
  "nickName": "testUsernick",
  "aboutMe": "",
  "birthday": 306536400
}
WS_ADD_CONTACT_PAYLOAD = {
    "action": "add_contact",
    "contactPhone": "9000000002"
    }
WS_CREATE_GROUP_PAYLOAD = {
  "action": "create_group_or_channel",
  "name_chat": "Test_group",
  "description": "Описание",
  "chat_type": "GROUP",
  "is_public": True,
  "participant_id": []
}
WS_CALL_ANSWER_PAYLOAD_TEMPLATE = {
   "action": "answer_call",
   "call_id": 10,
   "caller_phone_number": "9000000003",
   "sdp": "sdp-данные"
}

# Функция для динамического payload
def get_answer_payload(call_id):
    payload = WS_CALL_ANSWER_PAYLOAD_TEMPLATE.copy()  # создаем копию
    payload["call_id"] = call_id                     # подставляем актуальный ID
    return payload

