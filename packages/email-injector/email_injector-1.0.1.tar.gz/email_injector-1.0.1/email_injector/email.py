import base64
import json
import re
import time
from bs4 import BeautifulSoup
from typing import List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_injector import LocalGoogleInjector, GoogleAuth
from http_injector import HTTPInjector, TypeInjector

from .constant import Constant
from .utils import Line

class Email:
    
    @property
    def Connections(self):
        while True:
            try: return build('gmail', 'v1', credentials=Credentials(token=self.Auth))
            except HttpError: time.sleep(30)

    @property
    def getToken(self):
        while True:
            try:
                SERVICE = 'oauth2:https://www.googleapis.com/auth/dynamite https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/meetings https://www.googleapis.com/auth/hangouts https://www.googleapis.com/auth/chat.integration https://www.googleapis.com/auth/taskassist.readonly https://mail.google.com/ https://www.googleapis.com/auth/gmail.full_access https://www.googleapis.com/auth/gmail.ads https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/taskassist.readonly https://www.googleapis.com/auth/reminders https://www.googleapis.com/auth/gmail.locker.read https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/chat https://www.googleapis.com/auth/gmail.publisher_first_party https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/subscriptions https://www.googleapis.com/auth/peopleapi.readonly'
                CLIENT_SIG  = '38918a453d07199354f8b19af05ec6562ced5788'
                
                Auth = LocalGoogleInjector.GetIdToken(self.Email, self.Token, SERVICE, 'com.google.android.gm', CLIENT_SIG, self.deviceId)
                if not Auth.Error:
                    return Auth.Auth
                else:
                    raise Exception(Auth.Error)
            except HttpError: time.sleep(30)
    
    @property
    def get_mail_list(self) -> Constant.Response.ListEmail:
        while True:
            #try: return Constant.Response.ListEmail(self.Services.users().messages().list(userId='me', q='is:read').execute())
            try: return Constant.Response.ListEmail(self.Services.users().messages().list(userId='me', q='is:unread').execute())
            except HttpError as e: print(e); self.Services   = self.Connections
    
    @property
    def get_mail_content(self) -> Constant.Response.Contents:
        while True:
            try: 
                Result = self.Services.users().messages().get(userId='me', id=self.Messageid, format='full').execute()
                #json.dump(Result, open('Result.json', 'w'), indent=4)
                return Constant.Response.Contents(Result)
            except HttpError as e: print(e); self.Services   = self.Connections

    @property
    def unread_message(self):
        while True:
            try: return Constant.Response.Unread(self.Services.users().messages().modify(userId='me', id=self.Messageid,body={ 'removeLabelIds': ['UNREAD']}).execute())
            except HttpError as e: print(e); self.Services   = self.Connections
    
    def getTitle(self, headers: List[Constant.Response.Headers]):
        subject = None
        for header in headers:
            if header.name == 'Subject':
                subject = header.value
                break
        return subject
    
    def getDate(self, headers: List[Constant.Response.Headers]):
        subject = None
        for header in headers:
            if header.name == 'Date':
                subject = header.value
                break
        return subject
    
    @staticmethod
    def data_encoder(text)-> str:
        message = None
        if len(text)>0:
            message = base64.urlsafe_b64decode(text)
            message = str(message, 'utf-8')
        return message

    def read_message(self, payload: Constant.Response.Payload)->str:
        message = None
        if payload.body is not None:
            message = payload.body.data
            message = self.data_encoder(message)
        elif payload.parts is not None:
            message = payload.parts[0].body.data
            message = self.data_encoder(message)
        else:
            print("body has no data.")
        return message
    
    def ReadAll(self):
        Accounts = GoogleAuth.Select()
        for Account in Accounts:
            self.Token          = Account.Token
            self.deviceId       = Account.deviceId
            self.Email          = Account.Email
            self.Auth           = self.getToken
            self.Services       = self.Connections
            self.ListMessage    = self.get_mail_list
            if self.ListMessage.resultSizeEstimate > 0:
                Messages = self.ListMessage.messages
                if Messages is not None:
                    for Message in Messages:
                        self.Messageid = Message.id
                        content = self.get_mail_content
                        Title   = self.getTitle(content.payload.headers)
                        Line.Normal()
                        print(Title)
                        print(content.snippet)
                        if len(re.findall('BProgrammers Verification', Title)) > 0:
                            #print(content.snippet.split(' ')[8])
                            #print(Title.split('[')[1].split(']')[0])
                            print(self.getDate(content.payload.headers))
                        self.unread_message
    
    def ReadSpesifik(self, Email: str):
        Account = GoogleAuth.SelectBy(Email)
        if Account is not None:
            self.Token          = Account.Token
            self.deviceId       = Account.deviceId
            self.Email          = Account.Email
            self.Auth           = self.getToken
            self.Services       = self.Connections
            self.ListMessage    = self.get_mail_list
            if self.ListMessage.resultSizeEstimate > 0:
                Messages = self.ListMessage.messages
                if Messages is not None:
                    for Message in Messages:
                        self.Messageid = Message.id
                        content = self.get_mail_content
                        Title   = self.getTitle(content.payload.headers)
                        Line.Normal()
                        print(Title)
                        print(content.snippet)
                        self.unread_message
                        if len(re.findall('BProgrammers Verification', Title)) > 0:
                            #print(content.snippet.split(' ')[8])
                            #print(Title.split('[')[1].split(']')[0])
                            print(self.getDate(content.payload.headers))
                            try:
                                return int(Title.split('[')[1].split(']')[0])
                            except ValueError:
                                return content.snippet
        return None
    
    def ReadFaucetPay(self, Email: str):
        Account = GoogleAuth.SelectBy(Email)
        if Account is not None:
            self.Token          = Account.Token
            self.deviceId       = Account.deviceId
            self.Email          = Account.Email
            self.Auth           = self.getToken
            self.Services       = self.Connections
            self.ListMessage    = self.get_mail_list
            if self.ListMessage.resultSizeEstimate > 0:
                Messages = self.ListMessage.messages
                if Messages is not None:
                    for Message in Messages:
                        self.Messageid = Message.id
                        content = self.get_mail_content
                        Title   = self.getTitle(content.payload.headers)
                        Line.Normal()
                        print(Title)
                        print(content.snippet)
                        self.unread_message
                        if len(re.findall('Confirm your email address', Title)) > 0:
                            SOUP = BeautifulSoup(self.read_message(content.payload), 'lxml')
                            for LINK in SOUP.find_all('a'):
                                if len(re.findall('https://faucetpay.io/account/confirm-email', str(LINK))) > 0:
                                    HASH = str(LINK.text).split('/')[5]
                                    if len(HASH) >= len('d8430632fa78024e51475681ed2bc3aac7dea2e907fe3eec02bbdc9bc8b99a42'):
                                        return HASH
        return None
    
    def Activation(self, Email: str):
        client = HTTPInjector(
            TypeInjector.requests,
            30,
            {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Content-Type' : 'application/json'
            }
        )
        URL     = 'https://api.faucetpay.io/account/confirm-account'
        POST = dict(
            activation_hash = self.ReadFaucetPay(Email)
        )
        if POST['activation_hash'] is not None:
            
            Response = client.post(URL, json=POST).json()
            return Response
    
    def ReadFaucetPay2FA(self, Email: str):
        Account = GoogleAuth.SelectBy(Email)
        if Account is not None:
            self.Token          = Account.Token
            self.deviceId       = Account.deviceId
            self.Email          = Account.Email
            self.Auth           = self.getToken
            self.Services       = self.Connections
            self.ListMessage    = self.get_mail_list
            if self.ListMessage.resultSizeEstimate > 0:
                Messages = self.ListMessage.messages
                if Messages is not None:
                    for Message in Messages:
                        self.Messageid = Message.id
                        content = self.get_mail_content
                        Title   = self.getTitle(content.payload.headers)
                        if len(re.findall('2FA Authorization Code', Title)) > 0:
                            print(Title)
                            print(content.snippet)
                            return content.snippet.split(' ')[16]
        return None
    
    def __init__(self) -> None:
        pass
            