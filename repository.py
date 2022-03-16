import abc
import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.execute("INSERT INTO batches (reference, sku, _purchased_quantity, eta) "
                             "VALUES (:ref, :sku, :qty, :eta)",
                             dict(ref=batch.reference, sku=batch.sku, qty=batch.available_quantity, eta=batch.eta))

    def get(self, reference) -> model.Batch:
        resp = self.session.execute(
            "SELECT id, reference, sku, _purchased_quantity, eta FROM batches WHERE reference = :ref",
            dict(ref=reference)
        ).fetchone()

        b = model.Batch(ref=resp.reference, sku=resp.sku, qty=resp._purchased_quantity, eta=resp.eta)

        rows = list(self.session.execute(
            "SELECT sku, qty, orderid FROM order_lines WHERE "
            " id in ( SELECT orderline_id from allocations WHERE batch_id = :ref)",
            dict(ref=resp.id)))

        for r in rows:
            b.allocate(model.OrderLine(**r))
        return b
