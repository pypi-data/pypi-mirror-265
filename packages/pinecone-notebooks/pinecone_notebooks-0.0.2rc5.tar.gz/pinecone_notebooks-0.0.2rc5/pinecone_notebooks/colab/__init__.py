try:
  from google.colab import output
except:
  raise ImportError('This module is meant to be used in Google Colab.')
else:
  import os

  def SetApiKey(val):
    os.environ['PINECONE_API_KEY'] = val

  def Authenticate():
    apiKey = output.eval_js(
      'import {getPineconeApiKey} from "https://connect.pinecone.io/embed.js";' +
      'await getPineconeApiKey({integrationId: "colab"});'
    )
    return apiKey
