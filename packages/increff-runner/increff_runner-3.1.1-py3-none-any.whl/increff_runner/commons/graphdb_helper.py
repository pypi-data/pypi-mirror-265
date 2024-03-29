from neo4j import GraphDatabase
import configparser
from .constants import *

config = configparser.ConfigParser()
config.read('config.ini')

def create_algo_nodes(nodes,client,parallel_flag=0,count=1):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    for node in nodes:
        properties = f'{{name: "{node}", client: "{client}", parallel_flag: {parallel_flag}, count: {count}, last_block: 1, parent_task: "{node}"}}'
        query = session.run(f"merge (n:node{properties}) return n").data()
    return query

def connect_algo_nodes(node1,node2,client):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property1 = f'{{name: "{node1}", client: "{client}"}}'
    property2 = f'{{name: "{node2}", client: "{client}"}}'

    query = session.run(f"match (n1:node{property1}), (n2:node{property2}) merge (n1)-[:next]->(n2)").data()
    return query

def get_algo_node(node,client):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property = f'{{name: "{node}", client: "{client}"}}'
    query = session.run(f"match (n:node{property}) return n").data()
    return query[0]['n']

def get_next_algo_nodes(node,client):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property = f'{{name: "{node}", client: "{client}"}}'
    query = session.run(f"match (n:node{property})-[r:next]->(m) return m").data()
    next_nodes = []
    for node in query:
        next_nodes.append(node['m'])
    return next_nodes

def create_task_nodes(nodes,task_id,level,parent_task,last_block,block_identifier):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    for node in nodes:
        properties = f'{{name: "{node}", task_id: "{task_id}", level: "{level}", parent_task: "{parent_task}", last_block: "{last_block}", block_identifier: "{block_identifier}"}}'
        query = session.run(f"merge(n:node{properties}) return n").data()

    return query

def connect_task_nodes(task_id,node1,node2,level1,level2):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property1 = f'{{name: "{node1}", task_id: "{task_id}", level: "{level1}"}}'
    property2 = f'{{name: "{node2}", task_id: "{task_id}", level: "{level2}"}}'

    query = session.run(f"match (n1:node{property1}), (n2:node{property2}) merge (n1)-[:new]->(n2)").data()
    return query

def get_next_task_nodes(node,task_id,level):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property = f'{{name: "{node}", task_id: "{task_id}", level: "{level}"}}'
    query = session.run(f"match (n:node{property})-[r:new]->(m) return m").data()
    next_nodes = []
    for node in query:
        next_nodes.append(node['m'])

    return query

def get_task_node(node,task_id):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property = f'{{name: "{node}", task_id: "{task_id}"}}'
    query = session.run(f"match (n:node{property}) return n").data()
    return query[0]['n']

def get_no_of_parent_tasks(node,task_id,level):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property = f'{{name: "{node}", task_id: "{task_id}", level: "{level}"}}'
    query = session.run(f"match (n:node{property})<-[r]-(m) return count(r) as count").data()
    return query[0]['count']

def get_no_of_completed_parent_tasks(node,task_id,level):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property = f'{{name: "{node}", task_id: "{task_id}", level: "{level}"}}'
    query = session.run(f"match (n:node{property})<-[r:completed]-(m) return count(r) as count").data()
    return query[0]['count']

def add_caas_job_to_task_node(node,task_id,level,caas_job_id):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property = f'{{name: "{node}", task_id: "{task_id}", level: "{level}"}}'
    query = session.run(f"match (n:node{property}) set n.caas_job = '{caas_job_id}' return n").data()
    return query

def change_status_of_task_node(node,task_id,level,status):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property = f'{{name: "{node}", task_id: "{task_id}", level: "{level}"}}'
    query = session.run(f"match (n:node{property}) set n.status = '{status}' return n").data()
    return query

def check_last_block_status(task_id,node):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')
    
    property = f'{{task_id: "{task_id}", name: "{node}"}}'

    query = session.run(f"match (n:node{property}) return count(*) as count").data()
    total = query[0]['count']
    completed = session.run(f"match (n:node{property}) where n.status = 'SUCCESS' return count(*) as count").data()[0]['count']
    if total == completed:
        return True
    return False

def change_edge_between_task_nodes(node1,node2):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')
    query = session.run(f" match (n1:node{node1})-[old:`new`]->(n2:node{node2}) merge (n3:node{node1})-[fresh:`success`]->(n4:node{node2}) delete old").data()
   
def mark_all_dependants_as_failed(task_id):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    property = f'{{task_id: "{task_id}"}}'
    query = session.run(f"match(n:node{property}) where n.status<>'{SUCCESS}' set n.status='{FAILED}'").data()
    return query

def get_all_running_tasks_for_id(task_id):
    driver = GraphDatabase.driver(config['graphdb']['connection_string'], auth=(config['graphdb']['username'], config['graphdb']['password']))
    session = driver.session(database='neo4j')

    query = session.run(f"match(n:node) where n.task_id = '{task_id}' and exists(n.caas_job_id) and n.status<>'{SUCCESS}' return n").data()
    caas_ids = []
    for node in query:
        caas_ids.append(node['n']['caas_job_id'])

    return caas_ids