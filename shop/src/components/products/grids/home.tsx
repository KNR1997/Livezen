import { useProducts, useProducts_v2 } from '@/framework/product';
import { PRODUCTS_PER_PAGE } from '@/framework/client/variables';
import { Grid } from '@/components/products/grid';
import { useRouter } from 'next/router';
interface Props {
  className?: string;
  variables: any;
  column?: any;
  gridClassName?: string;
}
export default function ProductGridHome({
  className,
  variables,
  column,
  gridClassName,
}: Props) {
  const { query } = useRouter();

  const { products, loadMore, isLoadingMore, isLoading, hasMore, error } =
    useProducts({
      ...variables,
      ...(query.category && { categories: query.category }),
      ...(query.text && { name: query.text }),
    });

  // console.log('loadMore: ', loadMore)
  // console.log('isLoadingMore: ', isLoadingMore)

  // const { products_v2} =
  //   useProducts_v2({
  //     ...variables,
  //     ...(query.category && { categories: query.category }),
  //     ...(query.text && { name: query.text }),
  //   });

  const productsItem: any = products;
  // const productsItem_v2: any = products_v2;

  return (
      <Grid
        products={productsItem}
        loadMore={loadMore}
        isLoading={isLoading}
        isLoadingMore={isLoadingMore}
        hasMore={hasMore}
        error={error}
        limit={PRODUCTS_PER_PAGE}
        className={className}
        gridClassName={gridClassName}
        column={column}
      />
  );
}
