import express from 'express';
import createHttpError from 'http-errors';
import { logger } from './logger';
import * as ordersService from './domain/orders-service';

export function registerRoutes(app: express.Application) {
  const router = express.Router();

  router.post('/', async (req, res, next) => {
    try {
      logger.info({ body: req.body }, 'Creating order');
      const result = await ordersService.addOrder(req.body);
      res.status(201).json(result);
    } catch (error) {
      next(error);
    }
  });

  router.get('/:id', async (req, res, next) => {
    try {
      const order = await ordersService.getOrder(Number(req.params.id));
      if (!order) throw new createHttpError.NotFound();
      res.json(order);
    } catch (error) {
      next(error);
    }
  });

  router.delete('/:id', async (req, res, next) => {
    try {
      await ordersService.deleteOrder(Number(req.params.id));
      res.status(204).end();
    } catch (error) {
      next(error);
    }
  });

  app.use('/api/orders', router);
}
