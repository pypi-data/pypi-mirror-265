from ._core import FAISSVectorstore, OpenAILLM, OpenAITextEmbedder


class Ragasas:
    def __init__(
        self,
        api_key,
        data,
        retriever_message,
        system_message,
        embedding_model="text-embedding-ada-002",
        llm_model="gpt-3.5-turbo",
        output_vectorstore_absolute_path=None,
        save_to_cloud=False,
        metadatas=None,
    ):
        self.api_key = api_key
        self.data = data
        self.retriever_message = retriever_message
        self.system_message = system_message
        self.embedding_model = embedding_model
        self.llm_model = llm_model

        self.embedder = OpenAITextEmbedder(api_key=self.api_key)
        self.vector_store = FAISSVectorstore(self.embedder)
        self.vector_store.create_vector_store(
            self.data, output_vectorstore_absolute_path, save_to_cloud, metadatas
        )
        self.retriever = self.vector_store.as_retriever()
        self.llm = OpenAILLM(
            api_key,
            self.retriever,
            self.retriever_message,
            self.system_message,
        )

    def ask(self, message):
        response = self.llm.ask(message)
        return response
