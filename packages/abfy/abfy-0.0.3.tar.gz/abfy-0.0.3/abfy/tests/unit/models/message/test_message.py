from abfy.src.models.message.message import Message, MessageCollection


class TestResult:
    def test_message_collection_add_messages(self):
        message_collection = MessageCollection()

        message_collection.add_overall_message(Message(title="1"))
        message_collection.add_overall_message(Message(title="2"))
        message_collection.add_overall_message(Message(title="3"))

        message_collection.add_metric_message("col_1", Message(title="4"))
        message_collection.add_metric_message("col_1", Message(title="5"))
        message_collection.add_metric_message("col_2", Message(title="6"))

        assert len(message_collection.overall_messages) == 3
        assert len(message_collection.metric_messages) == 2
        assert len(message_collection.metric_messages["col_1"]) == 2
        assert len(message_collection.metric_messages["col_2"]) == 1

    def test_preprocess_pipeline_add_messages(self):
        message_collection1 = MessageCollection()
        message_collection2 = MessageCollection()

        message_collection1.add_overall_message(Message(title="1"))
        message_collection1.add_overall_message(Message(title="2"))
        message_collection1.add_overall_message(Message(title="3"))
        message_collection2.add_overall_message(Message(title="4"))

        message_collection1.add_metric_message("col_1", Message(title="4"))
        message_collection1.add_metric_message("col_2", Message(title="5"))
        message_collection1.add_metric_message("col_3", Message(title="6"))
        message_collection2.add_metric_message("col_1", Message(title="7"))

        message_collection1.combine(message_collection2)

        assert len(message_collection1.overall_messages) == 4
        assert len(message_collection1.metric_messages) == 3
        assert len(message_collection1.metric_messages["col_1"]) == 2
        assert len(message_collection1.metric_messages["col_2"]) == 1
        assert len(message_collection1.metric_messages["col_3"]) == 1
