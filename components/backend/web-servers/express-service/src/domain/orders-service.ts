export type OrderPayload = {
  id?: number;
  description: string;
  total: number;
};

const store: OrderPayload[] = [];
let counter = 1;

export async function addOrder(payload: OrderPayload) {
  const order = { ...payload, id: counter++ };
  store.push(order);
  return order;
}

export async function getOrder(id: number) {
  return store.find((item) => item.id === id) || null;
}

export async function deleteOrder(id: number) {
  const index = store.findIndex((item) => item.id === id);
  if (index >= 0) {
    store.splice(index, 1);
  }
}
