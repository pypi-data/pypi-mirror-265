import os
from dotenv import load_dotenv

import datetime

from neo4j import GraphDatabase
import neomodel as nm

from opentldr.Domain import *
from .log import log

load_dotenv()

def _getenv(variable:str , default:str):
        '''
        _getenv(variable, default) attempts to resolve the value of the environment variable specified.
        If it cannot find the variable in the OS or .env (from dotenv package) it will fail over to the
        provided default value while giving a warning to the logging system.
        '''
        value:str = os.getenv(variable)
        if value == None:
            log.warning("No environment variable '"+variable+"' so defaulting to '"+default+"'.")
            return default
        return value

class KnowledgeGraph:
    '''
    KnowledgeGraph is the API for OpenTLDR's interface to Neo4j graph database. It attempts to make the
    driver connection using OS, .env, and then default values for connections. This API maps neo4j
    nodes/edges to types specified in the Domain module (using Neomodel OGM and some custom cypher).

    In order to be successfull, you will need to have a neo4j server running, reachable on the network,
    and with environment variables (either in OS or .env files) similar to these:

        NEO4J_CONNECTION='bolt://localhost:7687'
        NEO4J_USERNAME=neo4jUser
        NEO4J_PASSWORD=neo4jPassword
        NEO4J_DATABASE=neo4j

    This class can be used in several different ways, including:
        (1) import opentldr.KnowledgeGraph ... kg=KnowledgeGraph() ... (use kg here) ... kg.close() 
        (2) with opentldr.KnowledgeGraph as kg: ... (use kg here, and then it will autoclose)

    '''

# -----------------
# Setup Methods
# -----------------

    # Default values come from first of: (1) .env file, (2) os environment, or (3) these hardcoded values
    connection=_getenv('NEO4J_CONNECTION','neo4j://localhost:7687')
    user= _getenv('NEO4J_USERNAME','neo4j')
    password= _getenv('NEO4J_PASSWORD','neo4jPassword')
    database= _getenv('NEO4J_DATABASE','neo4j')
    driver = GraphDatabase.driver(connection, auth=(user,password))
    nm.config.DRIVER = driver

    def __init__(self, neo4j_driver=None, connection=None, user=None, password=None, database=None):
        if connection is not None:
            self.connection=connection
        if user is not None:
            self.user=user
        if password is not None:
            self.password=password
        if database is not None:
            self.database=database
         
        if neo4j_driver is None:        
            log.info("Connecting to Neo4J using environment specification.")
            log.info("\tconnection:\t{v}".format(v=self.connection))
            log.info("\tuser:\t\t{v}".format(v=self.user))
            #log.info("\tpassword:\t{v}".format(v=self.password))
            log.info("\tdatabase:\t{v}".format(v=self.database))
            self.connect()
        else:
            log.info("Using Neo4j driver passed into initialization.")
            self.connect(neo4j_driver)

    def __del__(self):
        if self.driver is not None:
            self.driver.close()

    def __enter__(self):
        return self
    
    def __exit__(self,ctx_type, ctx_value, ctx_traceback):
        if self.driver is not None:
            self.driver.close()

# -----------------
# General Utility Methods
# -----------------

    def neo4j_query(self, cql):
        '''
        performs a cypher call to the knowledge base and returns results in the standard neo4j driver format.
        Use this if you are following neo4j documentation, otherwise use cypher_query().
        '''
        if self.driver == None:
            self.connect()

        try:
            records, summary, keys = self.driver.execute_query(cql, database_=self.database,)
            log.info("The query `{query}` returned {records_count} records in {time} ms.".format(
                query=summary.query, records_count=len(records),
                time=summary.result_available_after))
            return records, summary
        except Exception as e:
            log.error(e)

    def neomodel_query(self,cypher_query):
        '''
        performs a cypher query in the standard neomodel method, which will return a list of lists of neomodel.
        Use this if you are following Neomodel documentation, otherwise use cypher_query().
        '''
        if self.driver == None:
            self.connect()
        
        return nm.db.cypher_query(cypher_query, resolve_objects = True)

    def connect(self, driver=None):
        '''
        ensures that a connection to Neo4j has been established and is functioning.
        '''
        if driver==None:
            driver = GraphDatabase.driver(self.connection, auth=(self.user,self.password))
        
        log.info("Testing Neo4j Connectivity...")
        driver.verify_connectivity()
        
        if driver.verify_connectivity:
            log.info("Successfully connected to Neo4J server for KnowledgeGraph.")
        else:
            log.error("Unable to connect to Neo4J for KnowledgeGraph. Check that Neo4j server is running.")
            return False

        log.info("Testing Neo4j Authentication...")
        driver.verify_authentication()
        
        if driver.verify_authentication:
            log.info("Successfully logged into Neo4J server for KnowledgeGraph.")
        else:
            log.error("Unable to log in to Neo4J for KnowledgeGraph. Check that your user and password are correct.")
            return False
        
        self.driver=driver
        return True
    
    def getNeo4jDriver(self):
        '''
        returns the Neo4j driver class being used (usually neo4j.GraphDatabase.driver) so that direct neo4j calls can be
        made or it can be passed into other libraries.
        '''
        if self.driver==None:
            self.connect()
        return self.driver

    def close(self):
        '''
        shutsdown the current connection to neo4j. This should be done as the end of each program / notebook.
        If you use the "with statement" context control, this will be called automatically when the code block ends.
        '''
        if self.driver!=None:
            self.driver.close()
        self.driver=None

    def _ensure_saved(self,node:OpenTldrMeta):
        '''
        OpenTLDR objects all inherit from the OpenTldrMeta mixin class. They will be assigned a "uid" when they are saved.
        So, we can use this to determine if an object has been saved or not and respond appropriately.
        '''
        if node.uid is None:
            log.warn("Nodes must be persisted with node.save() before being connected. Forcing this now.")
            return node.save()
        return node


    def get_all_node_uids_by_tag(self, tag:str ) -> list[str]:
        '''
        returns the list of uids for the tag specified as a string.
        '''
        return self.cypher_query("MATCH (n:{tag}) RETURN n.uid".format(tag=tag))

    def get_all_nodes_by_tag(self, tag:str ):
        '''
        returns the list of uids for the tag specified as a string.
        '''
        return self.cypher_query("MATCH (n:{tag}) RETURN n".format(tag=tag),"n")


# -----------------
# KnowedgeGraph API 
# -----------------

    def cypher_query(self,cypher_query,extract_variable=None) ->list:
        '''
        performs a cypher query and returns a single simple list of Neomodel objects based on the variable indicated (or first).
        Use this for most OpenTLDR queries because it is much simpler to process for iterating on the results.
        For example: cypher_query("MATCH (a)-[b]->(c) RETURN a,b,c","a") only returns a list of only the "a" results.
        So, cypher_query("MATCH (a)-[b]->(c) RETURN a","a") would give the same result list by dropping the "b" and "c" results.
        '''
        if self.driver == None:
            self.connect()
        
        results, meta = nm.db.cypher_query(cypher_query, resolve_objects = True)
        
        index=0
        if extract_variable is not None:
            index=meta.index(extract_variable)
        else:
            if len(meta)>1:
                log.warn("cypher_query is defaulting to return the first element of multiple return values in results.")       
        
        return [item[index] for item in results]

    def cypher_query_one(self,cypher_query,extract_variable=None):
        '''
        performs a query that is intended to LIMIT the return values to one single Neomodel object. This simplifies the processing
        of the query results to consistently only get a single object for the extract_variable, it is undefined which unless you sort them.
        For example: cypher_query_one("MATCH (a)-[b]->(c) RETURN a,b,c","a") returns the FIRST object of result "a".
        So, cypher_query_one("MATCH (a)-[b]->(c) RETURN a LIMIT 1","a") gives the same result (faster).
        '''
        results = self.cypher_query(cypher_query,extract_variable)

        # Limits the output to the first actual object (i.e., not a list)        
        if results is not None and len(results)>0:
            return results[0]
        else:
            return None  
        
    def cypher_import(self,filename):
        '''
        processes a text file containing cypher commands and executes them on the KnowledgeGraph.
        '''
        count=0
        with open(filename) as fp:
            lines = fp.readlines()
            for line in lines:
                if len(line.strip()) == 0:
                    continue;   
                with self.driver.session() as session:
                    session.run(line)
                count=count+1
        log.info("Imported {count} lines of Cypher from {filename}".format(count=count, filename=filename))

    def delete_all(self):
        '''
        clears the neo4j graph database.
        '''
        self.cypher_query("MATCH(x) DETACH DELETE x")

    def shortest_path(self,start:OpenTldrMeta,end:OpenTldrMeta):
        '''
        this is a special cypher command to run neo4j's shortest path algorithm and return the path (list of edges) found.
        We remove EvalKey, Recommendation, Tldr, Source, and User nodes to avoid irrelevant paths that circumvent Reference Data.
        '''
        results,meta = self.neomodel_query("""
            MATCH path=shortestPath((s)-[*..10]-(e))
            WHERE s.uid='{start_id}'
            AND e.uid='{end_id}'                         
            AND NONE(n IN nodes(path) WHERE 'Recommendation' IN LABELS(n))
            AND NONE(n IN nodes(path) WHERE 'Tldr' IN LABELS(n))
            AND NONE(n IN nodes(path) WHERE 'Source' IN LABELS(n))
            AND NONE(n IN nodes(path) WHERE 'User' IN LABELS(n))
            AND NONE(n IN nodes(path) WHERE 'EvalKey' IN LABELS(n))
            RETURN path
            """.format(start_id=start.uid, end_id=end.uid))    
                     
        if len(results) == 0:
            return None
        else:
            return results[0][meta.index("path")]

    def get_by_uid(self, uid:str):
        return self.cypher_query_one("MATCH (n) WHERE n.uid='{uid}' RETURN n".format(uid=uid))

# -----------------
# Reference Data API
# -----------------

## Reference Nodes in KG these are labeled as ReferenceNode
         
    def add_reference_node(self, text:str, type:str, hypothesized:bool=False) -> ReferenceNode:
        '''
        creates a new ReferenceNode object in KG.
        '''
        return ReferenceNode(text=text, type=type, hypothesized=hypothesized).save()
    
    def update_reference_node(self, node:ReferenceNode) -> ReferenceNode:
        '''
        updates the KG with changes to a ReferenceNode properties
        '''
        return node.save()
    
    def delete_reference_node(self, node:ReferenceNode):
        '''
        removes the passed ReferenceNode and the edges connected to them.
        '''
        self.cypher_query("MATCH (n:ReferenceNode) WHERE n.uid='{uid}' DETACH DELETE n".format(uid=node.uid))
   
    def delete_all_reference_nodes(self):
        '''
        removes all of the ReferenceNode and the edges connected to them.
        '''
        self.cypher_query("MATCH (n:ReferenceNode) DETACH DELETE n")

    def get_reference_node_by_uid(self,uid:str) -> ReferenceNode:
        '''
        returns a single ReferenceNode as indicated by the uid or None if it does not exist in KG.
        '''
        return ReferenceNode.nodes.get_or_none(uid=uid);

    def get_all_reference_nodes(self) -> list[ReferenceNode]:
        '''
        returns a list of all the ReferenceNodes in the KG.
        '''
        return self.cypher_query("MATCH (n:ReferenceNode) RETURN n","n")

## Reference Edges - in KG these are labeled as REFERENCE_EDGE but Neomodel classes are ReferenceEdge
    
    def add_reference_edge(self, from_node:ReferenceNode, to_node:ReferenceNode, text:str, type:str, hypothesized:bool=False):
        '''
        adds a ReferenceEdge between two ReferenceNodes. Note these edges are only between ReferenceNodes.
        '''
        from_node:ReferenceNode=self._ensure_saved(from_node)
        to_node:ReferenceNode=self._ensure_saved(to_node)
        edge=from_node.edges.connect(to_node,{'type':type, 'text':text, 'hypothesized':hypothesized})
        return edge.save()
    
    def update_reference_edge(self, edge:ReferenceEdge) -> ReferenceEdge:
        '''
        updates the KG with changes to a ReferenceEdge's properties
        '''
        return edge.save()

    def delete_reference_edge(self, edge:ReferenceEdge):
        '''
        removes all ReferenceNode and the edges connected to them.
        '''
        self.cypher_query("MATCH (a)-[r:REFERENCE_EDGE]->(b) WHERE r.uid='{uid}' DETACH DELETE r".format(uid=edge.uid))

    def delete_all_reference_edges(self):
        '''
        removes all of the ReferenceEdges from KG.
        '''
        self.cypher_query("MATCH (a)-[r:REFERENCE_EDGE]->(b) DETACH DELETE r")

    def get_reference_edge_by_uid(self,uid:str) -> ReferenceEdge:
        '''
        returns a single ReferenceEdge as indicated by the uid or None if it does not exist in KG.
        '''
        self.cypher_query_one("MATCH (a)-[r:REFERENCE_EDGE]->(b) WHERE r.uid='{uid}' RETURN r".format(uid=uid))

    def get_all_reference_edges(self) -> list[ReferenceEdge]:
        '''
        returns a list of all of the ReferenceEdges in the KG.
        '''
        return self.cypher_query("MATCH (a)-[n:REFERENCE_EDGE]->(b) RETURN n","n")

# -----------------
# Active Data
# -----------------

## Source Nodes - refer to the origin of content
        
    def add_source(self, name:str) -> Source:
        '''
        creates new source node, or if one by the same name already exists it reuses it.
        '''
        source = Source.nodes.get_or_none(name=name)
        if source is None:
            source= Source(name=name).save()
        else:
            log.warn("Found existing Source node for name {name}, returning pre-existing node.".format(name=name))
        return source
    
    def update_source(self, node:Source) -> Source:
        '''
        updates the KG with changes to a Source properties
        '''
        return node.save()
    
    def delete_source(self, node:Source):
        '''
        removes the passed Source node and the edges connected to them.
        '''
        self.cypher_query("MATCH (n:Source) WHERE n.uid='{uid}' DETACH DELETE n".format(uid=node.uid))
   
    def delete_all_sources(self):
        '''
        removes all of the Sources and the edges connected to them.
        '''
        self.cypher_query("MATCH (n:Source) DETACH DELETE n")

    def get_source_by_uid(self, uid:str) -> Source:
        '''
        gets an existing Source node by uid or None if it does not exist
        '''
        return Source.nodes.get_or_none(uid=uid)
    
    def get_source_by_name(self, name:str) -> Source:
        '''
        gets an existing Source node by name or None if it does not exist
        '''
        return Source.nodes.get_or_none(name=name)
    
    def get_all_sources(self) -> list[Source]:
        return Source.nodes

## Content Nodes - contain article content and link to their Source

    def add_content(self, source:Source, type:str, url:str, date:datetime.date, title:str, text:str) -> Content:
        content = Content.nodes.get_or_none(url=url)
        if content is None:
            content=Content(url=url,date=date,title=title,text=text, type=type).save()
            content.is_from.connect(source)
        else:
            log.warn("Found existing Content node for url {url}, returning pre-existing node.".format(url=url))
        return content

    def get_all_content(self) -> list[Content]:
        content = Content.nodes
        return content

    def get_content_by_uid(self, uid:str) -> Content:
        content = Content.nodes.get_or_none(uid=uid)
        return content

    def get_content_by_url(self, url:str) -> Content:
        content = Content.nodes.get_or_none(url=url)
        return content

    def get_content_by_source(self,source:Source) -> list[Content]:
        return source.get_content()
    
    def get_content_by_date(self,date:datetime.date) -> list[Content]:
        content = Content.nodes.get_or_none(date=date)
        return content
    
    def get_content_by_title(self,title:str) -> Request:
       return self.cypher_query_one("""
            MATCH (c:Content) WHERE c.title='{title}'
            RETURN c """.format(title=title),"c")
    
    def get_content_by_recommendation(self,recommendation:Recommendation) -> list[Content]:
        return recommendation.get_content()
    
# Active Data / Entity
    
    def add_entity(self, content:Content, text:str, type:str ) -> Entity:
        entity=Entity(text=text,type=type).save()
        entity.mentioned_in.connect(content)
        return entity
    
    def add_refers_to_edge(self, entity:Entity, reference:ReferenceNode, confidence=1.0 ):
        entity.refers_to.connect(reference, {'confidence': confidence })

    def get_entity_by_uid(self, uid:str) -> Entity:
        entities = Entity.nodes.get_or_none(uid=uid)
        return entities
     
    def get_entity_by_url(self, url:str) -> Entity:
        entities = Entity.nodes.get_or_none(url=url)
        return entities
    
    def get_all_entities(self) -> list[Entity]:
        entities = Entity.nodes
        return entities

    def get_entities_by_content(self,content:Content) -> list[Entity]:
        return self.cypher_query("""
            MATCH (c:Content) WHERE c.uid='{content_uid}'
            MATCH (e:Entity)
            MATCH (e)-[y:MENTIONED_IN]->(c)
            RETURN e """.format(
                content_uid=content.uid),"e")

    def get_content_by_date(self,date:datetime.date) -> list[Content]:
        content = Content.nodes.get_or_none(date=date)
        return content

# -----------------
# Requests API 
# -----------------

# Users

    def add_user(self, name:str, email:str) -> User:
        user = User.nodes.get_or_none(name=name)
        if user is None:
            user=User(name=name, email=email).save()
        else:
            log.warn("Found existing User node for name {name}, returning pre-existing node.".
                      format(name=name))
        return user      

    def get_user_by_uid(self,uid:str) -> User:
        user = User.nodes.get_or_none(uid=uid)
        return user

    def get_user_by_name(self,name:str) -> User:
        user = User.nodes.get_or_none(name=name)
        return user


# Requests
    
    def add_request(self, title:str, text:str, user:User) -> Request:
        request = Request.nodes.get_or_none(title=title)
        if request is None or request.requested_by.single().uid != user.uid:
            request = Request(title=title, text=text).save()
            request.requested_by.connect(user)
        else:
            log.warn("Found existing Request node for {title}, returning pre-existing node.".format(title=title))
        return request

    def get_request_by_uid(self, uid:str) -> Request:
        request = Request.nodes.get_or_none(uid=uid)
        return request

    def get_request(self, name:str) -> Request:
        request = Request.nodes.get_or_none(name=name)
        return request
    
    def get_all_requests(self) -> list[Request]:
        requests = Request.nodes
        return requests
 
    def get_requests_by_user(self,user:User) -> list[Request]:
       return self.cypher_query("""
            MATCH (u:User) WHERE u.uid='{user_id}'
            MATCH (q:Request)
            MATCH (q)-[y:REQUESTED_BY]->(u)
            RETURN q """.format(
                user_id=user.uid),"q")
    
    def get_request_by_title(self,title:str) -> Request:
       return self.cypher_query_one("""
            MATCH (q:Request) WHERE q.title='{title}'
            RETURN q """.format(title=title),"q")

    def get_entities_by_request(self,request:Request) -> list[Entity]:
        return self.cypher_query("""
            MATCH (r:Request) WHERE r.uid='{request_uid}'
            MATCH (e:Entity)
            MATCH (e)-[y:MENTIONED_IN]->(r)
            RETURN e """.format(
                request_uid=request.uid),"e")

# -----------------
# Workflow Products API 
# -----------------

# Recommedations
    
    def add_recommendation(self, score:float, content:Content, request:Request) -> Recommendation:
        if content.uid is None or request.uid is None:
            log.error("Adding Recommendation requires an existing and saved Content and Request node. Attempting to save them...")
            content.save()
            request.save()
        
        recommendation = self.get_recommendation(content,request)
        if recommendation is None:
            recommendation= Recommendation(score=score).save()
            recommendation.recommends.connect(content)
            recommendation.relates_to.connect(request)
        else:
            log.warn("Found existing Recommendation node between content and request, returning pre-existing node.")
        return recommendation
    
    def get_recommendation_by_id(self, uid:str) -> Recommendation:
        recommendation = Recommendation.nodes.get_or_none(uid=uid)
        return recommendation

    def get_recommendation(self, content:Content, request:Request) -> Recommendation:      
        return self.cypher_query_one("""
            MATCH (q:Request) WHERE q.uid='{request_id}'
            MATCH (a:Content) WHERE a.uid='{content_id}'
            MATCH (r:Recommendation)
            MATCH (r)-[x:RECOMMENDS]->(a)
            MATCH (r)-[y:RELATES_TO]->(q)
            RETURN r LIMIT 1 """.format(
                request_id=request.uid,
                content_id=content.uid),"r")  

    def delete_recommendation(self, recommendation:Recommendation):
        recommendation.delete();
    
    def delete_all_recommendations(self):
        self.cypher_query("MATCH (r:Recommendation) DETACH DELETE (r)")
         
    def get_all_recommendations(self) -> list[Recommendation]:
        recommendations = Recommendation.nodes
        return recommendations
    
    def get_recommendations_by_request(self,request:Request) -> list[Recommendation]:
        return self.cypher_query("""
            MATCH (q:Request) WHERE q.uid='{request_id}'
            MATCH (r:Recommendation)
            MATCH (r)-[y:RELATES_TO]->(q)
            RETURN r ORDER BY r.score DESC """.format(
                request_id=request.uid),"r")

    # Summaries
    
    def add_summary(self, text:str, content:Content, recommendation:Recommendation=None) -> Summary:
        summary = self.get_summary(content,recommendation)
        if summary is None:
            summary= Summary(text=text).save()
            summary.summarizes.connect(content)
            if recommendation is not None:
                summary.focus_on.connect(recommendation)
        else:
            log.warn("Found existing Summary node, returning pre-existing node.")
        return summary
    
    def get_summary_by_id(self, uid:str) -> Summary:
        summary = Summary.nodes.get_or_none(uid=uid)
        return summary

    def get_summary(self, content:Content, recommendation:Recommendation) -> Summary:      
        return self.cypher_query_one("""
            MATCH (r:Recommendation) WHERE r.uid='{recommendation_id}'
            MATCH (a:Content) WHERE a.uid='{content_id}'
            MATCH (s:Summary)
            MATCH (s)-[x:SUMMARIZES]->(a)
            MATCH (s)-[y:FOCUS_ON]->(r)
            RETURN s """.format(
                recommendation_id=recommendation.uid,
                content_id=content.uid),"s")                 
    
    def get_summaries_by_content(self, content:Content) -> list[Summary]:      
        return self.cypher_query("""
            MATCH (a:Content) WHERE a.uid='{content_id}'
            MATCH (s:Summary)
            MATCH (s)-[x:SUMMARIZES]->(a)
            RETURN s """.format(content_id=content.uid))                 

    def get_summaries_by_recommendation(self, recommendation:Recommendation) -> list[Summary]:      
        return self.cypher_query("""
            MATCH (r:Recommendation) WHERE r.uid='{recommendation_id}'
            MATCH (s:Summary)
            MATCH (s)-[x:FOCUS_ON]->(r)
            RETURN s """.format(recommendation_id=recommendation.uid),"s")                 

    def get_all_summary(self) -> list[Summary]:
        summary = Summary.nodes
        return summary
    
# Tldr
    
    def add_tldr(self, request:Request, date:datetime.date) -> Tldr:
        tldr = self.get_tldr(request, date)
        if tldr is None:
            tldr= Tldr(date=date).save()
            tldr.response_to.connect(request)
        else:
            log.warn("Found existing Tldr node for request on given date, returning pre-existing node.")
        return tldr
    
    def add_entry_to_tldr(self, tldr:Tldr, score:float, recommendation:Recommendation, summary:Summary, content:Content) -> TldrEntry:
        tldr_entry=TldrEntry(link=content.url).save()
        tldr_entry.includes.connect(summary)
        tldr_entry.based_on.connect(recommendation)
        tldr.contains.connect(tldr_entry, {'score': score })

    def get_tldr_by_id(self, uid:str) -> Tldr:
        tldr = Tldr.nodes.get_or_none(uid=uid)
        return tldr

    def delete_tldr_entry(self, tldr_entry:TldrEntry):
        tldr_entry.delete()

    def delete_tldr(self, tldr:Tldr):
        for tldr_entry in tldr.contains.all():
            self.delete_tldr_entry(tldr_entry)
        tldr.delete()

    def delete_tldr_entries_by_tldr(self, tldr:Tldr):
        for tldr_entry in tldr.contains.all():
            self.delete_tldr_entry(tldr_entry)

    def delete_all_tldrs(self):
        for tldr in Tldr.nodes:
            self.delete_tldr(tldr)

    def get_tldrs_by_date(self, date:datetime.date):
        results = self.cypher_query("""
            MATCH (t:Tldr) WHERE t.date='{date}'
            RETURN t """.format(date=date),"t")
        if results is None:
            return None
        else:
            return results[0]

    def get_tldrs_before_date(self, date:datetime.date):
        return self.cypher_query("""
            MATCH (t:Tldr) WHERE t.date<'{date}'
            RETURN t """.format(date=date),"t")                 

    def get_all_tldrs(self) -> list[Tldr]:
        tldrs = Tldr.nodes
        return tldrs
    
    def get_entries_by_tldr(self, tldr:Tldr) -> list[TldrEntry]:
        return self.cypher_query("""
            MATCH (t:Tldr) WHERE t.uid='{tldr_id}'
            MATCH (e:TldrEntry)
            MATCH (t)-[x:CONTAINS]->(e)
            RETURN e ORDER BY e.score DESC""".format(tldr_id=tldr.uid),"e")                 

    def get_tldr_by_request(self,request:Request) -> list[Tldr]:
        return self.cypher_query("""
            MATCH (q:Request) WHERE q.uid='{request_id}'
            MATCH (t:Tldr)
            MATCH (t)-[y:RESPONSE_TO]->(q)
            RETURN t """.format(
                request_id=request.uid),"t")
    
    def get_tldr(self,request:Request, date:datetime.date) -> Tldr:
        return self.cypher_query_one("""
            MATCH (q:Request) WHERE q.uid='{request_id}'
            MATCH (t:Tldr) where t.date='{date}'
            MATCH (t)-[y:RESPONSE_TO]->(q)
            RETURN t """.format( date=date,
                request_id=request.uid),"t")


## EvalKey Nodes - rubric for evaluation metrics

    def add_evalkey(self, content:Content, request:Request, score:float, text:str) -> EvalKey:
        key = EvalKey(text=text, score=score).save()
        key.key_for_content.connect(content)
        key.key_for_request.connect(request)
        return key

    def get_all_evalkeys(self) -> list[EvalKey]:
        evalkeys = EvalKey.nodes
        return evalkeys

    def get_evalkey_by_uid(self, uid:str) -> Content:
        key = EvalKey.nodes.get_or_none(uid=uid)
        return key
    
    def get_evalkeys_by_request(self,request:Request) -> list[Content]:
        return self.cypher_query("""
            MATCH (q:Request) WHERE q.uid='{request_id}'
            MATCH (e:EvalKey)-[eq:KEY_FOR_REQUEST]->(q)
            RETURN e """.format(request_id=request.uid),"e")
    
    def get_evalkey_by_content_and_request(self, content:Content, request:Request) -> EvalKey:
        return self.cypher_query_one("""
            MATCH (c:Content) WHERE c.uid='{content_id}'
            MATCH (q:Request) WHERE q.uid='{request_id}'
            MATCH (c)<-[ec:KEY_FOR_CONTENT]-(e:EvalKey)-[eq:KEY_FOR_REQUEST]->(q)
            RETURN e """.format( content_id=content.uid, request_id=request.uid),"e")

    def delete_all_evalkeys(self):
        self.cypher_query("MATCH (r:EvalKey) DETACH DELETE (r)")
