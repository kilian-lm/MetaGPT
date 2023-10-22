## main.py
from flask import Flask, request, jsonify
from models import User, Project, Version
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from git_operations import GitOperations
from bigquery_operations import BigQueryOperations
from graph_generator import GraphGenerator
from api_chunker import ApiChunker

def create_app():
    app = Flask(__name__)

    # Initialize SQLAlchemy
    engine = create_engine('sqlite:///git_visualizer.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Initialize other modules
    git_ops = GitOperations()
    bq_ops = BigQueryOperations()
    graph_gen = GraphGenerator()
    api_chunker = ApiChunker()

    @app.route('/project', methods=['POST'])
    def create_project():
        try:
            data = request.get_json()
            user = User(id=data['user_id'], name=data['user_name'], email=data['user_email'])
            project = Project(id=data['project_id'], name=data['project_name'], user_id=data['user_id'], user=user)
            session.add(project)
            session.commit()
            return jsonify({'message': 'Project created successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/version', methods=['POST'])
    def create_version():
        try:
            data = request.get_json()
            project = session.query(Project).get(data['project_id'])
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            version = Version(id=data['version_id'], content=data['content'], timestamp=data['timestamp'], project_id=data['project_id'], project=project)
            session.add(version)
            session.commit()

            # Save the version to git and BigQuery
            git_ops.save_version(version)
            bq_ops.save_to_bigquery(version)

            return jsonify({'message': 'Version created successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/graph', methods=['GET'])
    def generate_graph():
        try:
            # Generate the graph
            graph = graph_gen.generate_graph()

            # Chunk the text and compare it
            chunked_text = api_chunker.chunk_text(graph)
            comparison_result = graph_gen.compare_text(chunked_text)

            return jsonify({'graph': graph, 'comparison_result': comparison_result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
