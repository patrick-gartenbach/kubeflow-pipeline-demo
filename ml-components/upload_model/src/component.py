import kfp.components as comp
def upload_model(minio_host,access_k,secret_k,bucket,name,dataset,model_path: comp.InputPath("XGBoost Model")):
    from minio import Minio
    import time
    import re
    from ml_metadata import metadata_store
    from ml_metadata.proto import metadata_store_pb2

    client = Minio(minio_host,
        access_key=access_k,
        secret_key=access_k,
        secure=False
    )
    time = int(time.time())
    client.fput_object(
            bucket, name+"-"+str(time), model_path,
        )
    METADATA_STORE_HOST = "metadata-grpc-service.kubeflow" # default DNS of Kubeflow Metadata gRPC service.
    METADATA_STORE_PORT = 8080
    mlmd_connection_config = metadata_store_pb2.MetadataStoreClientConfig(
        host=METADATA_STORE_HOST,
        port=METADATA_STORE_PORT,
    )
    store = metadata_store.MetadataStore(mlmd_connection_config)
    
    model_artifact = metadata_store_pb2.Artifact()
    model_artifact.uri = minio_host+"/"+bucket+"/"+name+"-"+str(time)
    model_artifact.properties["version"].int_value = time
    model_artifact.properties["name"].string_value = name
    model_artifact.properties["dataset"].string_value = dataset
    model_artifact.type_id = int(re.findall(r'\d+',str(store.get_artifact_type("TaxiMLModel")))[0])
    [model_artifact_id] = store.put_artifacts([model_artifact])