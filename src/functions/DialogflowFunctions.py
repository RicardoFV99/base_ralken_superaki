from typing import Dict, Any
from data.database import get_db_connection


## Capital Humano's main function
async def capitalHumanoFunc(responseId: str, queryResult: Dict[str, Any]):
    intent_name = queryResult.get('intent', {}).get('displayName', '')
    if intent_name == 'Inicio-Chat':
        return await handler_InicioChat(responseId)
    if intent_name == 'name_notrelated':
        return await handler_nameNotRelated(responseId, queryResult)
    if intent_name == 'Inicio-Nombre':
        return await handler_InicioNombre(responseId, queryResult)
    if intent_name == 'proceso_seleccion':
        return await handler_ProcesoSeleccion(responseId, queryResult)
    
    

async def handler_InicioChat(responseId: str):
    ## Get information from dialogflow to check if the responseId is presented in our database
    ## if responseId is presented then proceed to "inicio_nombre event response" 
    ## if not presented "name_notrelated"
    
    
    ## Once we have the database table create we can start fetching information from this one
    try:
        with await get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tabla_responsesId WHERE response_id = %s", (responseId,))
                result = cursor.fetchone()
        
                if result:

                    customer_name = result[1]
            
                    return {
                        "followupEventInput": {
                            "name": "inicio-nombre",
                            "parameters": {
                                "nombre": customer_name,
                                "parameter-name-2": "no parameter value"
                            },
                            "languageCode": "en-US" 
                        }
                    }
                else:
                    return {
                        "followupEventInput": {
                            "name": "name_notrelated",
                            "parameters": {
                            },
                            "languageCode": "en-US"
                        }
                    }
        cursor.close()
        connection.close()
            
    except Exception as error:
        return f"No pude conectarte a la base de datos error: {error}"
    

async def handler_nameNotRelated(responseId: str, queryResult: Dict[str, Any]):
    # if responseId is not presented then proceed to create a record with the data
    #Then proceed to "inicio_nombre" event response
    try:
        with await get_db_connection() as connection:
            with connection.cursor() as cursor:
                nombre = queryResult['parameters']['nombre']
                values = (responseId, nombre)
                #Insert the data
                cursor.execute("INSERT INTO tabla_responsesId (response_id, nombre) VALUES (%s, %s)", (values))
                #Confirm the changes
                connection.commit()
                return {
                    "followupEventInput": {
                        "name": "inicio-nombre",
                        "parameters": {
                            "nombre": nombre
                        },
                        "languageCode": "en-US" 
                    }
                }

        cursor.close()
        connection.close()
            
    except Exception as error:
        return f"No pude conectarte a la base de datos error: {error}"


async def handler_InicioNombre(responseId: str, queryResult: Dict[str, Any]):
    # Here we check if the queryResult contains the CPMexicano
    # if it contains the cp we proceed with "cm_identified" event
    # if not we proceed with cp_notidentified

    try:
        with await get_db_connection() as connection:
            with connection.cursor() as cursor:
                cp = queryResult['parameters']['cp_mexicano']
                values = (cp)
                #Insert the data
                cursor.execute("SELECT * FROM codigo_postal WHERE cp = {0}".format(cp))
                result = cursor.fetchone()
                #Confirm the changes
                if(result):
                    return {
                        "followupEventInput": {
                            "name": "cp_identified",
                            "parameters": {
                            },
                            "languageCode": "en-US" 
                        }
                    }
                else:
                    return {
                        "followupEventInput": {
                            "name": "cp_notidentified",
                            "parameters": {
                            },
                            "languageCode": "en-US" 
                        }
                    }
        cursor.close()
        connection.close()
            
    except Exception as error:
        return f"No pude conectarte a la base de datos error: {error}"



async def handler_ProcesoSeleccion(responseId: str, queryResult: Dict[str, Any]):
    # Here we check in the queryResult the parameter "codigo_postulante"
    # we query if it exists in the database, if exists we proceed to "proceso_identified"
    # if not we proceed with "proceso_notidentified"
    try:
        codigo_postulante = queryResult["parameters"]["codigo_postulante"]
        with await get_db_connection() as connection:
            with connection.cursor() as cursor:
                #query the data
                cursor.execute("SELECT * FROM proceso_reclutamiento_prueba WHERE codigo_reclutamiento = '{0}'".format(codigo_postulante))
                result = cursor.fetchone()
                if(result):
                    return {
                        "followupEventInput": {
                            "name": "proceso_identified",
                            "parameters": {
                                "nombre": result[1] + " " + result[2],
                                "status_reclutamiento": result[3],
                            },
                            "languageCode": "en-US" 
                        }
                    }
                else:
                    return {
                        "followupEventInput": {
                            "name": "proceso_notidentified",
                            "parameters": {
                            },
                            "languageCode": "en-US" 
                        }
                    }
            cursor.close()
            connection.close()    
    except Exception as error:
        return f"No pude conectarte a la base de datos error: {error}"