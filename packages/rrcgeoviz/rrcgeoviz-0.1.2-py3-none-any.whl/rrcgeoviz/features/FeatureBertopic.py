from rrcgeoviz.features.ParentGeovizFeature import ParentGeovizFeature
from nltk.corpus import stopwords
import panel as pn
import panel as pn
from rrcgeoviz.features.ParentGeovizFeature import ParentGeovizFeature


class FeatureBertopic(ParentGeovizFeature):
    def getOptionName(self):
        return "nlp_bertopics"

    def getRequiredColumns(self):
        return ["description_column"]

    def getHeaderText(self):
        return "Bertopics Intertopic Map"

    def _generateComponent(self):
        model = self.generated_data.data_dict["nlp_bertopics"]
        topics_df = model.get_topics()
        num_topics = len(topics_df)
        display_num_topics = pn.Column(
            f"The number of topics found by BERTopic is: {num_topics}"
        )
        top_ten_topics_info = pn.Column(
            model.get_topic_info()
            .head(10)
            .set_index("Topic")[["Count", "Name", "Representation"]]
        )

        bert = pn.Column(
            display_num_topics, top_ten_topics_info, model.visualize_topics()
        )
        return bert
