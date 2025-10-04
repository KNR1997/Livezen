import ProgressBox from '@/components/ui/progress-box/progress-box';
import { filterOrderStatus, ORDER_STATUS } from '@/utils/order-status';

import { OrderStatus, PaymentStatus } from '@/types';

interface Props {
  orderStatus?: OrderStatus;
  paymentStatus?: PaymentStatus;
}

const OrderStatusProgressBox = ({ paymentStatus, orderStatus }: Props) => {
  const currentStatusIndex = ORDER_STATUS.findIndex((o) => o.status === orderStatus) ?? 0;
  const filterStatus = filterOrderStatus(
    ORDER_STATUS,
    paymentStatus!,
    currentStatusIndex
  );

  console.log('Order status: ', orderStatus)
  console.log('filterStatus: ', filterStatus)
  console.log('currentStatusIndex: ', currentStatusIndex)

  return (
    <ProgressBox
      data={filterStatus}
      status={orderStatus!}
      filledIndex={currentStatusIndex}
    />
  );
};

export default OrderStatusProgressBox;
