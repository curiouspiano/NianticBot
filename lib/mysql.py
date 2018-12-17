#! /usr/bin/env python3

import asyncio
import aiomysql

class mysqldb:
        connection = None
        loop = None
        dbHost = ""
        dbUser = ""
        dbPass = ""
        dbName = ""

        def __init__(self, loop, host, user, password, name, connect=True):
                self.dbHost = host
                self.dbUser = user
                self.dbPass = password
                self.dbName = name
                print("mysqldb Object Initalized")
                if connect:
                        self.loop = loop

        async def init(self):
                await self.connect()

        def __del__(self):
                self.disconnect()

        async def connect(self):
                self.connection = await aiomysql.connect(host = self.dbHost,
                                                        port=3306,
                                                        user = self.dbUser,
                                                        password = self.dbPass,
                                                        db = self.dbName,
                                                        loop = self.loop)

        def disconnect(self):
                try:
                        if self.connection is not None:
                                self.connection.close()
                except:
                        pass


        async def fetch_all_list(self, result, key):
            result_list = []
            result = await result.fetchall()
            for i in result:
                result_list.append(i[key])
            return result_list

        async def query(self, query):
                #print('MYSQLDB: querying')
                cursor = await self.connection.cursor(aiomysql.cursors.DictCursor) #aiomysql.cursors.DictCursor
                #print("Query: %s\n"%query)
                await cursor.execute(query)
                await cursor.connection.commit()
                await cursor.close()
                return cursor
