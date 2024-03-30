
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

import time
from datetime import datetime
from importlib.metadata import version
from flask import Blueprint , render_template , request , g as _g 
from esanom import database as _database , util as _util , config as _config
from . import common as _common 

#####################################################################

ROUTES = Blueprint( "routes" , __name__ , template_folder = "templates" , static_folder='static' )

#####################################################################

@ROUTES.before_request
def before_request_func( ) :
    _g._benchmark_before_request = time.time( )

@ROUTES.after_request
def after_request_func( resp ) :

    if "text/html" not in resp.headers[ "Content-Type" ] : return( resp )

    cookie_key = request.cookies.get( "key" , "" )
    #if cookie_key.strip( ) != "" : return( resp )
    if len( cookie_key ) == 64 : return( resp )

    ####

    session_key = _util.generate_rhash( )
    resp.set_cookie( "key" , session_key , secure = True , samesite = "Strict" )

    ####

    return( resp )

#####################################################################

@ROUTES.route( "/error_404" , methods = [ "GET" ] )
def page_error_404( ) :
    return( render_template( "error_404.html" ) , 404 )

@ROUTES.route( "/error_500" , methods = [ "GET" ] )
def page_error_500( ) :
    return( render_template( "error_500.html" ) , 500 )

#####################################################################

@ROUTES.app_context_processor
def app_context_processor( ) :

    # FIXME TODO should be optimized
    system_databaseversion_row = _database.db_query_select_row( "SELECT * from `system` WHERE `key`=%s LIMIT 1" , [ "database/version" ] )
    system_orchestratortime_row = _database.db_query_select_row( "SELECT * from `system` WHERE `key`=%s LIMIT 1" , [ "orchestrator/time" ] )
    system_schedulertime_row = _database.db_query_select_row( "SELECT * from `system` WHERE `key`=%s LIMIT 1" , [ "scheduler/time" ] )

    orchestrator_time_dt = round( time.time( ) - system_orchestratortime_row[ "val_int" ] )
    scheduler_time_dt = round( time.time( ) - system_schedulertime_row[ "val_int" ] )

    api_row = _database.db_query_select_row( "SELECT * from `api` WHERE `name` LIKE '%0_USER' LIMIT 1" )

    flag_sampledata = False 
    if api_row != None : flag_sampledata = True

    data = {
        "config_data" : _config.DATA ,
        "nom_version" : version( "esanom" ) ,
        "database_version" : system_databaseversion_row[ "val_str" ] ,
        "orchestrator_time_dt" : orchestrator_time_dt ,
        "scheduler_time_dt" : scheduler_time_dt ,
        "year" : datetime.now( ).strftime( "%Y" ) ,
        "flag_sampledata" : flag_sampledata ,
        "benchmark" : round( time.time( ) - _g._benchmark_before_request , 3 )
    }

    return( dict( _tdata = data ) )

@ROUTES.app_template_global( "test" )
def app_template_global_test( n ) :
    return( f"{n}." )

#####################################################################

@ROUTES.route( "/" , methods = [ "GET" ] )
def page_index( ) :

    return( render_template( "page_index.html" ) )

@ROUTES.route( "/docs" , methods = [ "GET" ] )
def page_docs( ) :
    return( render_template( "page_docs.html" ) )

@ROUTES.route( "/models" , methods = [ "GET" ] )
def page_models( ) :

    rolemodel_rows = _database.db_query_select_rows( "SELECT * from `rolemodel` where enable=1" )

    for rolemodel_row in rolemodel_rows :
        if rolemodel_row[ "heartbeat_at" ] != None :
            rolemodel_row[ "[heartbeat_last]" ] = round( time.time( ) - rolemodel_row[ "heartbeat_at" ].timestamp( ) )
        else :
            rolemodel_row[ "[heartbeat_last]" ] = 99999

    columns = [ "uid" , "name" , "category" , "desc" , "[heartbeat_last]" ]

    tdata = {
        "rows" : rolemodel_rows ,
        "columns" : columns
    }

    return( render_template( "page_models.html" , tdata = tdata ) )

@ROUTES.route( "/model" , methods = [ "GET" ] )
def page_model( ) :

    rolemodel_uid = _common.request_arg_str( "rolemodel_uid" )

    rolemodel_row = _database.db_query_select_row( "SELECT * from `rolemodel` WHERE uid=%s LIMIT 1" , [ rolemodel_uid ] )

    if rolemodel_row == None : return( render_template( "error_500.html" ) )

    ####

    mport_rows = _database.db_query_select_rows( "SELECT id,port_id,direction,enable,cardinal from mport where rolemodel_id=%s order by id" , [ rolemodel_row[ "id" ] ] )

    ####

    has_inputs = False
    has_outputs = False

    mpins = [ ]

    for mport_row in mport_rows :

        if mport_row["direction"] == "inputs" : has_inputs = True 
        if mport_row["direction"] == "outputs" : has_outputs = True 
        
        port_row = _database.db_query_select_row( "SELECT * from port where id=%s LIMIT 1" , [ mport_row[ "port_id" ] ] )

        mport_row[ "[port_name]"] = port_row[ "name" ]
        mport_row[ "[port_uid]"] = port_row[ "uid" ]

        mpin_rows = _database.db_query_select_rows( "SELECT id,mport_id,unit_id from mpin where mport_id=%s order by id" , [ mport_row["id"] ] )


        for mpin_row in mpin_rows :
            unit_row = _database.db_query_select_row( "SELECT * from unit where id=%s LIMIT 1" , [ mpin_row["unit_id"]] )
            pin_row = _database.db_query_select_row( "SELECT * from pin where id=%s LIMIT 1" , [ unit_row["pin_id"]] )
            port_pin_row = _database.db_query_select_row( "SELECT * from port_pin where port_id=%s and pin_id=%s LIMIT 1" , [port_row[ "id" ] , pin_row[ "id" ] ] )
            mpin_row[ "cardinal" ] = port_pin_row[ "cardinal" ]
            mpin_row[ "id" ] = pin_row[ "id" ]
            mpin_row[ "name" ] = pin_row[ "name" ]
            mpin_row[ "type" ] = pin_row[ "type" ]
            mpin_row[ "unit_name" ] = unit_row[ "name" ]
            mpin_row[ "port_name/pin_name(unit_name)" ] = port_row[ "name" ] + "/" + pin_row[ "name" ] + "(" + unit_row[ "name" ] + ")"


        mpins.append( mpin_rows )

        mport_row[ "[mpin_rows]" ] = mpin_rows


    mpin_columns = [ "name" , "cardinal" , "type" , "unit_name" ]

    tdata = {
        "row" : rolemodel_row ,
        "mport_rows" : mport_rows ,
        "has_inputs" : has_inputs ,
        "has_outputs" : has_outputs ,
        "mpin_columns" : mpin_columns
    }

    return( render_template( "page_model.html" , tdata = tdata ) )



@ROUTES.route( "/login" , methods = [ "GET" ] )
def page_login( ) :
    return( render_template( "page_login.html" ) )
    
#####################################################################

@ROUTES.route( "/admin_pipelines" , methods = [ "GET" ] )
def page_admin_pipelines( ) :

    pipeline_rows = _database.db_query_select_rows( "SELECT * from pipeline ORDER by id DESC" )

    #print(pipeline_rows)

    for pipeline_row in pipeline_rows :
        pipeline_obj = _database.pipeline_object( pipeline_row )
        #pipeline_obj.print_debug( )
        pipeline_row[ "[nodes]" ] = pipeline_obj.nodes



    cols = [ "uid" , "name" , "status" , "done" , "archived" , "[nodes]" ]

    tdata = {
        "rows" : pipeline_rows ,
        "cols" : cols
    }


    return( render_template( "page_admin_pipelines.html" , tdata = tdata ) )


@ROUTES.route( "/dashboard_tasks" , methods = [ "GET" ] )
def page_dashboard_tasks( ) :

    tdata = {
    }


    return( render_template( "page_dashboard_tasks.html" , tdata = tdata ) )


#####################################################################

@ROUTES.route( "/admin/db_rolemodel_rows" , methods = [ "GET" ] )
def admin_db_rolemodel_rows( ) :

    rolemodel_rows = _database.db_query_select_rows( "SELECT id,api_id,name,enable,updateable from rolemodel order by id" )

    print(rolemodel_rows)

    for rolemodel_row in rolemodel_rows :

        rolemodel_api_id = rolemodel_row[ "api_id" ]

        if rolemodel_api_id == None : continue

        api_row = _database.db_query_select_row( "SELECT * from api where id=%s LIMIT 1" , [ rolemodel_api_id ] )
        api_name = api_row[ "name" ]
        if api_name.startswith( "test_" ) : api_name = api_name[ -10: ]

        rolemodel_row[ "[api_name]" ] = api_name
        rolemodel_row[ "[api_enable]" ] = api_row[ "enable" ]

    tdata = {
        "rolemodel_rows" : rolemodel_rows
    }
    print(tdata)

    return( render_template( "db_rolemodel_rows.html" , tdata = tdata ) )

@ROUTES.route( "/admin/db_rolemodel_row" , methods = [ "GET" ] )
def admin_db_rolemodel_row( ) :

    rolemodel_id = _common.request_arg_int( "rolemodel_id" )

    ####

    rolemodel_row = _database.db_query_select_row( "SELECT id,api_id,name,enable,updateable from rolemodel where id=%s" , [ rolemodel_id ] )

    mport_rows = _database.db_query_select_rows( "SELECT id,port_id,direction,enable,cardinal from mport where rolemodel_id=%s order by id" , [ rolemodel_id ] )

    mpins = [ ]
    for mport_row in mport_rows :
        port_row = _database.db_query_select_row( "SELECT * from port where id=%s LIMIT 1" , [ mport_row["port_id"]] )
        port_name = port_row[ "name" ]
        mport_row[ "[port_name]" ] = port_name

        mpin_rows = _database.db_query_select_rows( "SELECT id,mport_id,unit_id from mpin where mport_id=%s order by id" , [ mport_row["id"] ] )

        for mpin_row in mpin_rows :
            unit_row = _database.db_query_select_row( "SELECT * from unit where id=%s LIMIT 1" , [ mpin_row["unit_id"]] )
            pin_row = _database.db_query_select_row( "SELECT * from pin where id=%s LIMIT 1" , [ unit_row["pin_id"]] )
            port_pin_row = _database.db_query_select_row( "SELECT * from port_pin where port_id=%s and pin_id=%s LIMIT 1" , [port_row[ "id" ] , pin_row[ "id" ] ] )
            mpin_row[ "[direction]" ] = mport_row[ "direction" ]
            mpin_row[ "[port_pin_cardinal]" ] = port_pin_row[ "cardinal" ]
            mpin_row[ "[pin_id]" ] = pin_row[ "id" ]
            mpin_row[ "[port_name/pin_name(unit_name)]" ] = port_row[ "name" ] + "/" + pin_row[ "name" ] + "(" + unit_row[ "name" ] + ")"


        mpins.append( mpin_rows)


    tdata = {
        "rolemodel_row" : rolemodel_row ,
        "mport_rows" : mport_rows ,
        "mpins" : mpins
    }

    return( render_template( "db_rolemodel_row.html" , tdata = tdata ) )

####

@ROUTES.route( "/admin/db_pipeline_rows" , methods = [ "GET" ] )
def admin_db_pipeline_rows( ) :

    pipeline_rows = _database.db_query_select_rows( "SELECT id,roleuser_id,name,status,done,archived,created_at,updated_at from pipeline order by id DESC" )

    tdata = {
        "pipeline_rows" : pipeline_rows
    }

    return( render_template( "admin_db_pipeline_rows.html" , tdata = tdata ) )

@ROUTES.route( "/admin/db_pipeline_row" , methods = [ "GET" ] )
def admin_db_pipeline_row( ) :
    pipeline_id = _common.request_arg_int( "pipeline_id" )
    pipeline_row = _database.db_query_select_row( "SELECT * from pipeline where id=%s" , [pipeline_id] )

    pipeline_object = _database.pipeline_object(pipeline_row)

    tdata = {
        "pipeline_row" : pipeline_row ,
        "pipeline" : pipeline_object
    }
    pipeline_object.print_debug()
    return( render_template( "admin_db_pipeline_row.html" , tdata = tdata ) )


@ROUTES.route( "/hx_test" , methods = [ "POST" ] )
def hx_test( ) :

    tdata = {
        "k1" : time.time( )
    }
    return( render_template( "hx_test.html" , tdata = tdata ) )



@ROUTES.route( "/hx_dashboard_tasks_taskcount" , methods = [ "GET" ] )
def hx_dashboard_tasks_taskcount( ) :

    task_rows = _database.db_query_select_rows( "SELECT * from task where done=%s" , [ 0 ] )

    tdata = {
        "x" : datetime.now().isoformat() ,
        "y" : len( task_rows )
    }
    return( render_template( "hx_dashboard_tasks_taskcount.html" , tdata = tdata ) )

