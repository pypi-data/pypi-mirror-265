
#################################################################################
#
# {___     {__          {__       {__
# {_ {__   {__          {_ {__   {___
# {__ {__  {__   {__    {__ {__ { {__
# {__  {__ {__ {__  {__ {__  {__  {__
# {__   {_ {__{__    {__{__   {_  {__
# {__    {_ __ {__  {__ {__       {__
# {__      {__   {__    {__       {__
#
# (C) Copyright European Space Agency, 2024
# 
# This file is subject to the terms and conditions defined in file 'LICENCE.txt', 
# which is part of this source code package. No part of the package, including 
# this file, may be copied, modified, propagated, or distributed except 
# according to the terms contained in the file ‘LICENCE.txt’.“ 
#
#################################################################################

import os
import sys
import json
import jsonschema
from . import util as _util

#####################################################################

NOM_CONFIG_PATH = "nom_config.json"

DATA = { }

DATA_SCHEMA = {

    "type" : "object" ,
    "properties" : {

        "database" : {

            "type" : "object" ,
            "additionalProperties" : False ,
            "required" : [ "host" , "port" , "user" , "passwd" , "database" ] ,
            "properties" : {

                "host" : { "type" : "string" } ,
                "port" : { "type" : "string" } ,
                "user" : { "type" : "string" } ,
                "passwd" : { "type" : "string" } ,
                "database" : { "type" : "string" }

            } ,

        } ,

        "fs_storage_path" : { "type" : "string" } ,
        "cache_filepath" : { "type" : "string" } ,
        "admin_api_email" : { "type" : "string" } ,
        "admin_api_ip" : { "type" : "string" } 

    }

}

#####################################################################

def init( ) :

    global DATA

    cwd_fp = os.getcwd( )

    NOM_CONFIG_PATH2 = NOM_CONFIG_PATH

    if "NOM_CONFIG_PATH" in os.environ :
        NOM_CONFIG_PATH2 = os.environ[ "NOM_CONFIG_PATH" ]
        print( f"CONFIG LOADED FROM ENV {NOM_CONFIG_PATH2}")



    config_fp = f"{NOM_CONFIG_PATH2}"
    if not NOM_CONFIG_PATH2.startswith("/"):
        config_fp = f"{cwd_fp}/{NOM_CONFIG_PATH2}"

    ####

    if load_from_filepath( config_fp ) == None :
        if load_from_env( ) == None :
            raise Exception( f"Unable to init env" )

    ####

    try :
        jsonschema.validate( instance = DATA , schema = DATA_SCHEMA )
    except jsonschema.ValidationError as e :
        raise Exception( f"CONFIG validate DATA_SCHEMA jsonschema.exceptions.ValidationError {e}" )

    DATA[ "_package_fp" ] = os.path.abspath( os.path.dirname( __file__ ) )
    DATA[ "_cwd_fp" ] = cwd_fp

    if "fs_storage_path" not in DATA : DATA[ "fs_storage_path" ] = "/tmp/nom"
    DATA[ "fs_storage_path" ].rstrip( "/" )

    ####

    # Flag for flask server debug

    config_init_default_boolean( "server_debug" )
    config_init_default_boolean( "server_security_lax" )
    config_init_default_boolean( "database_disable_init" )


    ####

    #_util.print_debug( DATA )

    if DATA.get( "server_endpoint" , " " ).startswith( "http://" ) :
        print( "WARNING server_endpoint http in use" )

    return( True )

#####################################################################

def config_init_default_boolean( k , v = False ) :
    global DATA

    if k not in DATA :
        DATA[ k ] = v
        return

    if DATA[ k ] == "y" :
        DATA[ k ] = True
    else :
        DATA[ k ] = False


#__SERVER_SECURITY_TOKENLAX__


#####################################################################

def load_from_filepath( config_fp ) :
    global DATA

    if not os.path.isfile( config_fp ) :
        print( f"WARNING CONFIG FILE NOT FOUND {config_fp=}" )
        return( None )

    ####

    with open( config_fp ) as f :
        try :
            DATA = json.loads( f.read( ) )
            print( f"Config loaded from file config_fp = {config_fp}" )
            return( True )
        except json.decoder.JSONDecodeError as e :
            print( f"ERROR JSONDecodeError {e.msg}" )
            sys.exit( 4 )

def load_from_env( ) :

    db_host = os.environ.get( "DB_HOST" , None )
    db_port = os.environ.get( "DB_PORT" , None )
    db_user = os.environ.get( "DB_USER" , None )
    db_passwd = os.environ.get( "DB_PASSWD" , None )
    db_database = os.environ.get( "DB_DATABASE" , None )

    admin_api_email = os.environ.get( "NOM_ADMIN_API_EMAIL" , "nom@sparc.space" )
    server_endpoint = os.environ.get( "NOM_CONFIG_SERVER_ENDPOINT" , "http://127.0.0.1:13031/v3/api/" )
    server_token = os.environ.get( "NOM_CONFIG_SERVER_TOKEN" , "admin" )

    global DATA

    DATA = {

        "database" : {
            "host" : db_host ,
            "port" : db_port ,
            "user" : db_user ,
            "passwd" : db_passwd ,
            "database" : db_database 
        } ,

        "admin_api_email" : admin_api_email,
        "server_endpoint" : server_endpoint ,
        "server_token" : server_token

    }

    _util.print_debug( DATA , "Config loaded from ENV" )


    if db_host == None or db_port == None : return( None )
    if db_user == None or db_passwd == None : return( None )
    if db_database == None : return( None )

    if admin_api_email == None : return( None )

    return( True )


def update( fp ) :
    global DATA

    if not os.path.isfile( fp ) : raise Exception( f"FILE NOT FOUND {fp}" )

    with open( fp ) as f :
        try :
            data = json.loads( f.read( ) )
            DATA.update( data )
            print( f"Config updated" )
        except json.decoder.JSONDecodeError as e :
            raise Exception( f"ERROR JSONDecodeError {e.msg}" )



#####################################################################

def val( k ) :
    return( f"{k}...bar" )

def get( k ) :
    return( DATA.get( k , None ) )

def print_debug( ) :
    _util.debug_json_print( DATA )

