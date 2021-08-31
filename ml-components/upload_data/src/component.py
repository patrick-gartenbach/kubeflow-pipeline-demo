
def upload_data(minio_host,access_k,secret_k,bucket,name,train_data_path: comp.InputPath("CSV"),test_data_path: comp.InputPath("CSV")) -> str:
    from minio import Minio
    import time
    from ml_metadata import metadata_store
    from ml_metadata.proto import metadata_store_pb2

    client = Minio(minio_host,
        access_key=access_k,
        secret_key=access_k,
        secure=False
    )
    time = int(time.time())
    client.fput_object(
            bucket, name+"-train-"+str(time), train_data_path,
        )
    client.fput_object(
            bucket, name+"-test-"+str(time), test_data_path,
        )
    
    # connect to metastore
    METADATA_STORE_HOST = "metadata-grpc-service.kubeflow" # default DNS of Kubeflow Metadata gRPC service.
    METADATA_STORE_PORT = 8080
    mlmd_connection_config = metadata_store_pb2.MetadataStoreClientConfig(
        host=METADATA_STORE_HOST,
        port=METADATA_STORE_PORT,
    )
    store = metadata_smodel_type.properties["name"] = metadata_store_pb2.STRING

    
    train_data_artifact = metadata_store_pb2.Artifact()
    train_data_artifact.uri = minio_host+"/"+bucket+"/"+name+"-train-"+str(time)
    train_data_artifact.properties["version"].int_value = time
    train_data_artifact.properties["name"].string_value = name
    train_data_artifact.properties["split"].string_value = "train"
    train_data_artifact.properties["horizen"].string_value = "2018 Jan - 2018 Feb"
    train_data_artifact.type_id = int(re.findall(r'\d+',str(store.get_artifact_type("TaxiDataset")))[0])    
    model_artifact = metadata_store_pb2.Artifact()
    test_data_artifact.uri = minio_host+"/"+bucket+"/"+name+"-test-"+str(time)
    test_data_artifact.properties["version"].int_value = time
    test_data_artifact.properties["name"].string_value = name
    test_data_artifact.properties["split"].string_value = "test"
    test_data_artifact.properties["horizen"].string_value = "2018 Jan - 2018 Feb"
    test_artifact.type_id = int(re.findall(r'\d+',str(store.get_artifact_type("TaxiDataset")))[0])
    [train_data_artifact_id] = store.put_artifacts([train_data_artifact,artifact])
    return minio_host+"/"+bucket+"/"+name+"-train-"+str(time)