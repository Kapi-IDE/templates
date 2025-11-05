import { FastifyInstance } from 'fastify';
import createHttpError from 'http-errors';
import * as ordersService from './domain/orders-service';

export async function registerRoutes(app: FastifyInstance) {
  app.get('/health', async () => ({ status: 'ok' }));

  app.post('/api/orders', async (request, reply) => {
    const order = await ordersService.addOrder(request.body as any);
    reply.code(201).send(order);
  });

  app.get('/api/orders', async (_request, reply) => {
    const orders = await ordersService.listOrders();
    reply.send(orders);
  });

  app.delete('/api/orders/:id', async (request, reply) => {
    const id = Number((request.params as { id: string }).id);
    if (Number.isNaN(id)) throw new createHttpError.BadRequest('Invalid id');
    await ordersService.deleteOrder(id);
    reply.code(204).send();
  });
}
